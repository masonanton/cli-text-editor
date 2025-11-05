import curses

KEYS = {
    "CTRL_Q": 17,
    "CTRL_S": 19,
    "CTRL_Z": 26,
    "CTRL_Y": 25,
    "ENTER": 10,
    "BACKSPACE": 8,
    "DELETE": 127,
    "TAB": 9,
    "ARROWS": (
        curses.KEY_UP,
        curses.KEY_DOWN,
        curses.KEY_LEFT,
        curses.KEY_RIGHT,
    ),
    "DELETION": (
        8,
        127,
        curses.KEY_BACKSPACE,
    ),
}
