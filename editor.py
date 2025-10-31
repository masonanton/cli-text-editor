import curses
import sys
from buffer import TextBuffer
from commands import NewLineCommand, DeleteCharCommand, InsertCharCommand
from history import History
from keys import KEYS
from cursor import Cursor

#TODO: refactor. maybe everything is an action where we pass in the key stroke, 
# and then use a factory pattern
class Editor:
    def __init__(self, stdscr, filename):
        self.stdscr = stdscr
        self.filename = filename
        self.buffer = TextBuffer(filename)
        self.cursor = Cursor()
        self.history = History()

    def run(self):
        curses.curs_set(1) # show the cursor
        self.stdscr.keypad(True)

        while True:
            self.render()
            key = self.stdscr.getch()

            if key == KEYS["CTRL_Q"]:
                break
            elif key == KEYS["CTRL_S"]:
                if not self.filename:
                    self.filename = self.prompt_filename("Save as: ")
                    if not self.filename:
                        continue
                self.buffer.save_file(self.filename)
                max_y, _ = self.stdscr.getmaxyx()
                self.stdscr.addstr(max_y - 1, 0, f"Saved to {self.filename}".ljust(60))
                self.stdscr.refresh()
                curses.napms(800) 
            elif key in KEYS["ARROWS"]:
                self.cursor.move(key, self.buffer)
            elif key == KEYS["ENTER"]:
                cmd = NewLineCommand(self.cursor.row, self.cursor.col)
                self.cursor.update(cmd.do(self.buffer))
                self.history.record(cmd)
            elif key in KEYS["DELETION"]:
                if self.cursor.col == 0 and self.cursor.row == 0:
                    continue
                cmd = DeleteCharCommand(self.cursor.row, self.cursor.col)
                self.cursor.update(cmd.do(self.buffer))
                self.history.record(cmd)
            elif 32 <= key <= 126:
                char = chr(key)
                cmd = InsertCharCommand(self.cursor.row, self.cursor.col, char)
                self.cursor.update(cmd.do(self.buffer))
                self.history.record(cmd)
            elif key == KEYS["CTRL_Z"]:
                new_location = self.history.undo(self.buffer)
                if new_location != (-1, -1):
                    self.cursor.update(new_location)
            elif key == KEYS["CTRL_Y"]:
                new_location = self.history.redo(self.buffer)
                if new_location != (-1, -1):
                    self.cursor.update(new_location)

    def render(self):
        self.stdscr.clear()

        # TODO: draw buffer.text (list of lines)
        for i, line in enumerate(self.buffer.lines):
            self.stdscr.addstr(i, 0, line)
        
        self.stdscr.move(self.cursor.row, self.cursor.col)
        self.stdscr.refresh()

    # def move_cursor(self, key):
    #     if key == curses.KEY_UP and self.cursor_row > 0:
    #         self.cursor_row -= 1
    #     elif key == curses.KEY_DOWN and self.cursor_row < len(self.buffer.lines) - 1:
    #         self.cursor_row += 1
    #     elif key == curses.KEY_LEFT: 
    #         if self.cursor_col > 0:
    #             self.cursor_col -= 1
    #         elif self.cursor_row > 0:
    #             prev_line_length = self.buffer.get_prev_line_length(self.cursor_row)
    #             self.cursor_row -= 1
    #             self.cursor_col = prev_line_length
    #     elif key == curses.KEY_RIGHT:
    #         if self.cursor_col < len(self.buffer.lines[self.cursor_row]):
    #             self.cursor_col += 1
    #         elif self.cursor_row < len(self.buffer.lines) - 1:
    #             self.cursor_row += 1
    #             self.cursor_col = 0

    #     # Clamp horizontal cursor if line is shorter
    #     current_line = self.buffer.lines[self.cursor_row]
    #     if self.cursor_col > len(current_line):
    #         self.cursor_col = len(current_line)

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