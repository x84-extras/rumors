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
