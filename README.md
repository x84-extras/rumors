# x/84 Rumors

Adds Ami/X style "rumors" to your system.

## Installation

### As a git project

You can keep up to date with changes if you clone this project into a
subdirectory of your `scriptpath`:

    $ cd /path/to/scripts
	$ git clone https://github.com/x84-extras/rumors

The rumors script is now being exposed as its own Python module.

When you use `gosub`, reference it like this:

```python
gosub('rumors/rumors')
```

#### A step further: submodules

If your `scriptpath` is already a git repo unto itself, then you can make it
very easy to stay up to date with various x/84 mods if you add them as
*git submodules*:

    $ cd /path/to/scripts
	$ git submodule add https://github.com/x84-extras/rumors rumors

It clones the repo just like `git clone` would do. However, it's been flagged
as a *submodule*, and so the batch commands that act on submodules can now
be used to do things like update all of your submodules at once:

    $ cd /path/to/scripts
	$ git submodule update --init --remote --recursive

### As plain files

You don't have to use git to use this script. Simply download the raw files
from the github website. Copy `rumors.py` into your `scriptpath` and copy
`art/rumors.ans` into your `art` folder.

To launch the rumors menu, use `gosub`:

```python
gosub('rumors')
```

## Using rumors in your layouts

To pull a rumor at random for display in your menu:

```python
from rumors import get_rumor
rumor = get_rumor()
```

This method will work if you're using this script as a git project or not.

## Configuration

There are a number of options you can use to customize the rumors script to
your system. Use the following options in the `[rumors]` section of your
`default.ini` file:

- `default_rumor` - The rumor to use when the database is empty
- `art_file` - The path to the ANSI banner for the rumors menu
- `show_menu_entries` - Whether or not menu entries should be sent to output
- `menu_highlight_color` - Highlight color for the menu entries
- `menu_lowlight_color` - Lowlight color for the menu entries
- `menu_command_text` - Text for the command prompt
- `menu_command_color` - Color for the command prompt text
- `menu_prompt_color` - Color for the command prompt editor
- `list_border_color` - Border color for the rumors list lightbar
- `list_highlight_color` - Highlight color for the rumors list lightbar
- `add_prompt_color` - Color for the 'add rumor' editor
- `delete_prompt_color` - Color for the 'delete a rumor' editor
