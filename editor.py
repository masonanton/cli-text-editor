import curses
import sys
from core.buffer import TextBuffer
from commands import NewLineCommand, DeleteCharCommand, InsertCharCommand
from core.history import History
from utils.keys import KEYS
from utils.words import english_words
from core.cursor import Cursor
from strategies.key import EnterKeyStrategy, InsertKeyStrategy, DeleteKeyStrategy, MoveKeyStrategy
from strategies.ctrl import UndoCtrlKeyStrategy, RedoCtrlKeyStrategy, SaveCtrlKeyStrategy

#TODO: refactor. maybe everything is an action where we pass in the key stroke, 
# and then use a factory pattern
class Editor:
    def __init__(self, stdscr, filename):
        self.stdscr = stdscr
        self.filename = filename
        self.buffer = TextBuffer(filename)
        self.cursor = Cursor()
        self.history = History()
        self.ghost_text = ""
        self.word_cache = {}

    def run(self):
        curses.curs_set(1) # show the cursor
        self.stdscr.keypad(True)
        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(1, 8, -1)

        while True:
            self.render()
            key = self.stdscr.getch()

            if key == KEYS["CTRL_Q"]:
                break
            elif key == KEYS["CTRL_S"]:
                SaveCtrlKeyStrategy().execute(self)
                curses.napms(800) 
            elif key in KEYS["ARROWS"]:
                MoveKeyStrategy().execute(self, key)
            elif key == KEYS["ENTER"]:
                EnterKeyStrategy().execute(self)
            elif key in KEYS["DELETION"]:
                DeleteKeyStrategy().execute(self)
            elif 32 <= key <= 126:
                InsertKeyStrategy().execute(self, key)
            elif key == KEYS["CTRL_Z"]:
                UndoCtrlKeyStrategy().execute(self)
            elif key == KEYS["CTRL_Y"]:
                RedoCtrlKeyStrategy().execute(self)
            
            prev_word = self.buffer.get_word_before_cursor(self.cursor.row, self.cursor.col)
            self.ghost_text = self.autocomplete(prev_word) if prev_word else ""

    def render(self):
        self.stdscr.clear()

        for i, line in enumerate(self.buffer.lines):
            self.stdscr.addstr(i, 0, line)

        if self.ghost_text:
            self.stdscr.addstr(self.cursor.row, self.cursor.col, self.ghost_text, curses.color_pair(1))
        
        self.stdscr.move(self.cursor.row, self.cursor.col)
        self.stdscr.refresh()

    def autocomplete(self, prev_word):
        if prev_word in self.word_cache:
            word = self.word_cache[prev_word]
        else:
            word = next((w for w in english_words if w.startswith(prev_word) and w != prev_word), "")
            self.word_cache[prev_word] = word

        if word:
            return word[len(prev_word):] 
        return ""

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