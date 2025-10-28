class TextBuffer:
    def __init__(self):
        # TODO: load a provided file
        self.lines = [
            "Hello, world!",
            "This is a test.",
            "Cursor movement check.",
            "Short",
            "A much longer line to test bounds",
        ]

    def insert_char(self, row, col, char):
        line = self.lines[row]
        self.lines[row] = line[:col] + char + line[col:]

    def delete_char(self, row, col):
        if col > 0:
            line = self.lines[row]
            self.lines[row] = line[:col - 1] + line[col:]
        elif row > 0:
            prev = self.lines[row - 1]
            self.lines[row - 1] = prev + self.lines[row]
            del self.lines[row]

    def insert_newline(self, row, col):
        line = self.lines[row]
        self.lines[row] = line[:col]
        self.lines.insert(row + 1, line[col:])

    def get_prev_line_length(self, row):
        return len(self.lines[row - 1])