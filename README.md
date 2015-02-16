# x/84 Rumors

Adds Ami/X style "rumors" to your system.

## Installation

Copy `rumors.py` into your `scriptpath` and copy `art/rumors.ans` into your
`art` folder. To pull a rumor for incorporating into your system's menus,
you can use the following code snippet:

```python
from rumors import get_rumor
rumor = get_rumor()
```

When launched with `gosub`, the file will act as a stand-alone rumors menu.

## Configuration

There are a number of options you can use to customize the rumors script to
your system. Use the following options in the `[rumors]` section of your
`default.ini` file:

- `default_rumor` - The rumor to use when the database is empty
- `art_file` - The path to the ANSI banner for the rumors menu
- `menu_highlight_color` - Highlight color for the menu entries
- `menu_lowlight_color` - Lowlight color for the menu entries
- `menu_command_text` - Text for the command prompt
- `menu_command_color` - Color for the command prompt text 
- `menu_prompt_color` - Color for the command prompt editor
- `list_border_color` - Border color for the rumors list lightbar
- `list_highlight_color` - Highlight color for the rumors list lightbar
- `add_prompt_color` - Color for the 'add rumor' editor
- `delete_prompt_color` - Color for the 'delete a rumor' editor
