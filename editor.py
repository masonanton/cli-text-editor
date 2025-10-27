import curses
from buffer import TextBuffer

CTRL_Q_KEY = 17 # Ctrl + Q ASCII
ARROW_KEYS = (curses.KEY_UP, curses.KEY_DOWN, curses.KEY_LEFT, curses.KEY_RIGHT)
class Editor:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.buffer = TextBuffer()
        self.cursor_row = 0
        self.cursor_col = 0

    def run(self):
        curses.curs_set(1) # show the cursor
        self.stdscr.keypad(True)

        while True:
            self.render()
            key = self.stdscr.getch()

            if key == CTRL_Q_KEY:
                break
            elif key in ARROW_KEYS:
                self.move_cursor(key)
            else:
                # TODO: insert text logic
                pass

    def render(self):
        self.stdscr.clear()

        # TODO: draw buffer.text (list of lines)
        for i, line in enumerate(self.buffer.lines):
            self.stdscr.addstr(i, 0, line)
        
        self.stdscr.move(self.cursor_row, self.cursor_col)
        self.stdscr.refresh()

    def move_cursor(self, key):
        if key == curses.KEY_UP and self.cursor_row > 0:
            self.cursor_row -= 1
        elif key == curses.KEY_DOWN and self.cursor_row < len(self.buffer.lines) - 1:
            self.cursor_row += 1
        elif key == curses.KEY_LEFT and self.cursor_col > 0:
            self.cursor_col -= 1
        elif key == curses.KEY_RIGHT and self.cursor_col < len(self.buffer.lines[self.cursor_row]):
            self.cursor_col += 1

        # Clamp horizontal cursor if line is shorter
        current_line = self.buffer.lines[self.cursor_row]
        if self.cursor_col > len(current_line):
            self.cursor_col = len(current_line)

        # TODO: left at col 0 moves to previous line, right at end moves to next

def main(stdscr):
    Editor(stdscr).run()

if __name__ == "__main__":
    curses.wrapper(main)