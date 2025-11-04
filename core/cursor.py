import curses

class Cursor:
    def __init__(self):
        self.row = 0
        self.col = 0

    def update(self, new_location):
        self.row, self.col = new_location

    def move(self, key, buffer):
        if key == curses.KEY_UP and self.row > 0:
            self.row -= 1

        elif key == curses.KEY_DOWN and self.row < len(buffer.lines) - 1:
            self.row += 1

        elif key == curses.KEY_LEFT:
            if self.col > 0:
                self.col -= 1
            elif self.row > 0:
                prev_line_length = buffer.get_prev_line_length(self.row)
                self.row -= 1
                self.col = prev_line_length

        elif key == curses.KEY_RIGHT:
            if self.col < len(buffer.lines[self.row]):
                self.col += 1
            elif self.row < len(buffer.lines) - 1:
                self.row += 1
                self.col = 0

        # Clamp column to current line length
        current_line = buffer.lines[self.row]
        if self.col > len(current_line):
            self.col = len(current_line)