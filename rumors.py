""" Rumors script for x/84. """
# https://github.com/x84-extras/rumors
__author__ = u'haliphax <https://github.com/haliphax>'

# std imports
import collections
import os

# local
from x84.bbs import getsession, getterminal, DBProxy
from x84.bbs.ini import get_ini
from x84.bbs.output import echo

MYDIR = os.path.dirname(__file__)

# settings - configured in default.ini [rumors] section
DEFAULT_RUMOR = get_ini('rumors', 'default_rumor') or \
    u'No rumors; why not add one yourself?'
ART_FILE = get_ini('rumors', 'art_file') or \
    (u'art/rumors.ans' \
    if not (os.path.isdir(os.path.join(MYDIR, '.git')) \
            or os.path.isdir(os.path.join(MYDIR, '_git'))) \
    else os.path.join(MYDIR, 'art', 'rumors.ans'))
SHOW_MENU_ENTRIES = get_ini('rumors', 'show_menu_entries',
                            getter='getboolean')
MENU_HIGHLIGHT_COLOR = get_ini('rumors', 'menu_highlight_color') or \
    u'bold_green'
MENU_LOWLIGHT_COLOR = get_ini('rumors', 'menu_lowlight_color') or \
    u'bold_black'
MENU_COMMAND_TEXT = get_ini('rumors', 'menu_command_text') or \
    u'command'
MENU_COMMAND_COLOR = get_ini('rumors', 'menu_command_color') or \
    u'bold_green'
MENU_PROMPT_COLOR = get_ini('rumors', 'menu_prompt_color') or \
    u'black_on_green'
LIST_BORDER_COLOR = get_ini('rumors', 'list_border_color') or \
    u'bold_black'
LIST_HIGHLIGHT_COLOR = get_ini('rumors', 'list_highlight_color') or \
    u'bold_white_on_green'
ADD_PROMPT_COLOR = get_ini('rumors', 'add_prompt_color') or \
    u'bold_white_on_green'
DELETE_PROMPT_COLOR = get_ini('rumors', 'delete_prompt_color') or \
    u'bold_white_on_green'


# namedtuple for our menu entries (to be used in render_menu_entries)
MenuItem = collections.namedtuple('MenuItem', ['inp_key', 'text'])


def get_rumor():
    """ Pull a rumor from the database (or default if none are found). """
    import random

    rumordb = DBProxy('rumors')
    rumor = DEFAULT_RUMOR
    keys = rumordb.keys()

    if keys:
        rumor = rumordb[random.choice(keys)]

    return rumor


def add_rumor():
    """ Add a new rumor to the database. """
    from x84.bbs.editor import ScrollingEditor

    term = getterminal()
    led = ScrollingEditor(width=term.width + 1, xloc=-1,
                          yloc=term.height, max_length=128,
                          colors={'highlight':
                                  getattr(term, ADD_PROMPT_COLOR)})
    echo(led.refresh())
    rumor = led.read()
    echo(term.normal)

    if rumor:
        rumordb = DBProxy('rumors')

        with rumordb:
            key = 1
            if len(rumordb):
                key = int(max(rumordb.keys())) + 1
            rumordb['%d' % key] = rumor


def view_rumors():
    """ View list of rumors. """
    from x84.bbs.lightbar import Lightbar

    session, term = getsession(), getterminal()
    rumordb = DBProxy('rumors')
    lbar = Lightbar(width=term.width - 1, height=term.height, xloc=0, yloc=0,
                    colors={'border': getattr(term, LIST_BORDER_COLOR),
                            'highlight': getattr(term, LIST_HIGHLIGHT_COLOR)},
                    glyphs={'top-left': u'+', 'top-right': u'+',
                            'top-horiz': u'-', 'bot-horiz': u'-',
                            'bot-left': u'+', 'bot-right': u'+',
                            'left-vert': u'|', 'right-vert': u'|'})

    def refresh():
        """ Refresh the lightbar. """
        if not len(rumordb):
            return False

        contents = [(key, '{key}) {rumor}'.format(key=key, rumor=rumordb[key]))
                    for key in sorted(rumordb.keys())]
        lbar.update(contents)
        echo(u''.join([lbar.border(), lbar.refresh()]))

    refresh()

    while not lbar.quit:
        event, data = session.read_events(['refresh', 'input'])

        if event == 'refresh':
            refresh()
        elif event == 'input':
            session.buffer_input(data, pushback=True)
            echo(lbar.process_keystroke(term.inkey()))


def del_rumor():
    """ Delete a rumor from the database. """
    from x84.bbs.editor import LineEditor

    session, term = getsession(), getterminal()
    rumordb = DBProxy('rumors')
    echo(u'\r\n\r\n')

    if not session.user.is_sysop:
        echo(u'Only SysOps can do that!')
        term.inkey()
        return

    led = LineEditor(width=len(str(max(rumordb.keys()))),
                     colors={'highlight':
                             getattr(term, DELETE_PROMPT_COLOR)})
    echo(u''.join([term.move_x(max(term.width / 2 - 40, 0)), 'Delete rumor: ',
                   led.refresh()]))

    try:
        rumor = int(led.read())
    except (ValueError, TypeError):
        rumor = None

    echo(term.normal)

    if rumor:
        rumordb = DBProxy('rumors')

        with rumordb:
            del rumordb['%d' % rumor]


def main():
    """ x/84 script launch point. """
    from x84.bbs.editor import LineEditor
    from common import (display_banner,   # pylint: disable=W0403
                        render_menu_entries)

    session, term = getsession(), getterminal()
    session.activity = u'Browsing rumors'

    def refresh():
        """ Refresh the menu. """

        echo(term.clear)
        top_margin = display_banner(ART_FILE) + 1
        echo(u'\r\n')

        if SHOW_MENU_ENTRIES:
            colors = {'highlight': getattr(term, MENU_HIGHLIGHT_COLOR),
                      'lowlight': getattr(term, MENU_LOWLIGHT_COLOR)}
            entries = [
                MenuItem(inp_key=u'v', text=u'view rumors'),
                MenuItem(inp_key=u'a', text=u'add a rumor'),
                MenuItem(inp_key=u'q', text=u'quit to main'),
            ]

            if session.user.is_sysop:
                entries.append(MenuItem(inp_key=u'd', text=u'delete a rumor'))

            echo(render_menu_entries(term, top_margin, entries, colors))

        echo(u'{0}[{1}]: {2}'.format(term.move_x(max(term.width / 2 - 40,
                                                     0))
                                     if term.width > 80 else u'',
                                     getattr(term, MENU_COMMAND_COLOR)
                                     (MENU_COMMAND_TEXT),
                                     led.refresh()))

    led = LineEditor(width=1, colors={'highlight':
                                      getattr(term, MENU_PROMPT_COLOR)})
    dirty = True
    event = None

    # input loop
    while True:
        if dirty or event == 'refresh':
            dirty = False
            refresh()

        event, data = session.read_events(['input', 'refresh'])

        if event == 'input':
            session.buffer_input(data, pushback=True)
            echo(led.process_keystroke(term.inkey(0)))

            if not led.carriage_returned:
                continue

            dirty = True
            echo(term.normal)
            inp = led.content
            led.content = u''
            led._carriage_returned = False

            if inp:
                inp = inp.lower()

                if inp == u'a':
                    add_rumor()
                elif inp == u'v':
                    view_rumors()
                elif inp == u'd':
                    del_rumor()
                elif inp == u'q':
                    return
