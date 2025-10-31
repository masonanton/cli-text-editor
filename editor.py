import curses
import sys
from buffer import TextBuffer
from commands import NewLineCommand, DeleteCharCommand, InsertCharCommand
from history import History

CTRL_Q_KEY = 17 
CTRL_S_KEY = 19
CTRL_Z_KEY = 26
CTRL_Y_KEY = 25
ENTER_KEY = 10
BACKSPACE_KEY = 8
DELETE_KEY = 127
ARROW_KEYS = (curses.KEY_UP, curses.KEY_DOWN, curses.KEY_LEFT, curses.KEY_RIGHT)
DELETION_KEYS = (BACKSPACE_KEY, DELETE_KEY, curses.KEY_BACKSPACE)
#TODO: refactor. maybe everything is an action where we pass in the key stroke, 
# and then use a factory pattern
class Editor:
    def __init__(self, stdscr, filename):
        self.stdscr = stdscr
        self.filename = filename
        self.buffer = TextBuffer(filename)
        #TODO: make cursor a class
        self.cursor_row = 0
        self.cursor_col = 0
        self.history = History()

    def run(self):
        curses.curs_set(1) # show the cursor
        self.stdscr.keypad(True)

        while True:
            self.render()
            key = self.stdscr.getch()

            if key == CTRL_Q_KEY:
                break
            elif key == CTRL_S_KEY:
                if not self.filename:
                    self.filename = self.prompt_filename("Save as: ")
                    if not self.filename:
                        continue
                self.buffer.save_file(self.filename)
                max_y, _ = self.stdscr.getmaxyx()
                self.stdscr.addstr(max_y - 1, 0, f"Saved to {self.filename}".ljust(60))
                self.stdscr.refresh()
                curses.napms(800) 
            elif key in ARROW_KEYS:
                self.move_cursor(key)
            elif key == ENTER_KEY:
                cmd = NewLineCommand(self.cursor_row, self.cursor_col)
                self.cursor_row, self.cursor_col = cmd.do(self.buffer)
                self.history.record(cmd)
            elif key in DELETION_KEYS:
                if self.cursor_col == 0 and self.cursor_row == 0:
                    continue
                cmd = DeleteCharCommand(self.cursor_row, self.cursor_col)
                self.cursor_row, self.cursor_col = cmd.do(self.buffer)
                self.history.record(cmd)
            elif 32 <= key <= 126:
                char = chr(key)
                cmd = InsertCharCommand(self.cursor_row, self.cursor_col, char)
                self.cursor_row, self.cursor_col = cmd.do(self.buffer)
                self.history.record(cmd)
            elif key == CTRL_Z_KEY:
                new_row, new_col = self.history.undo(self.buffer)
                if (new_row, new_col) != (-1, -1):
                    self.cursor_row, self.cursor_col = new_row, new_col
            elif key == CTRL_Y_KEY:
                new_row, new_col = self.history.redo(self.buffer)
                if (new_row, new_col) != (-1, -1):
                    self.cursor_row, self.cursor_col = new_row, new_col

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
        elif key == curses.KEY_LEFT: 
            if self.cursor_col > 0:
                self.cursor_col -= 1
            elif self.cursor_row > 0:
                prev_line_length = self.buffer.get_prev_line_length(self.cursor_row)
                self.cursor_row -= 1
                self.cursor_col = prev_line_length
        elif key == curses.KEY_RIGHT:
            if self.cursor_col < len(self.buffer.lines[self.cursor_row]):
                self.cursor_col += 1
            elif self.cursor_row < len(self.buffer.lines) - 1:
                self.cursor_row += 1
                self.cursor_col = 0

        # Clamp horizontal cursor if line is shorter
        current_line = self.buffer.lines[self.cursor_row]
        if self.cursor_col > len(current_line):
            self.cursor_col = len(current_line)

    def prompt_filename(self, prompt_text="Save as: "):
        curses.echo()  # show typed characters
        max_y, _ = self.stdscr.getmaxyx()

        # Clear last line
        self.stdscr.move(max_y - 1, 0)
        self.stdscr.clrtoeol()

        # Show prompt
        self.stdscr.addstr(max_y - 1, 0, prompt_text)
        self.stdscr.refresh()

        # Read input from user
        filename = self.stdscr.getstr(max_y - 1, len(prompt_text), 100)
        curses.noecho()

        # Convert from bytes to str
        return filename.decode("utf-8").strip()


def main(stdscr):
    filename = sys.argv[1] if len(sys.argv) > 1 else None
    Editor(stdscr, filename).run()

if __name__ == "__main__":
    curses.wrapper(main)