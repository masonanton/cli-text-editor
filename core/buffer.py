class TextBuffer:
    def __init__(self, filename = None):
        self.lines = [""]

        if filename:
            self.load_file(filename)

    def insert_char(self, row, col, char):
        line = self.lines[row]
        self.lines[row] = line[:col] + char + line[col:]

    def delete_char(self, row, col):
        # Case 1: delete within the same line
        if col > 0:
            line = self.lines[row]
            deleted_char = line[col - 1]
            self.lines[row] = line[:col - 1] + line[col:]
            return deleted_char

        # Case 2: at start of line, merge with previous
        elif row > 0:
            prev_line = self.lines[row - 1]
            deleted_char = "\n"
            self.lines[row - 1] = prev_line + self.lines[row]
            del self.lines[row]
            return deleted_char

        return None


    def insert_newline(self, row, col):
        line = self.lines[row]
        self.lines[row] = line[:col]
        self.lines.insert(row + 1, line[col:])
    
    def load_file(self, filename):
        try:
            with open(filename, 'r', encoding="utf-8-sig") as file:
                self.lines = [line.rstrip("\n") for line in file.readlines()]
        except FileNotFoundError:
            print(f"Error: The file ${filename} was not found.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def save_file(self, filename):
        with open(filename, 'w', encoding="utf-8-sig") as f:
            for line in self.lines:
                f.write(line + "\n")

    def get_prev_line_length(self, row):
        return len(self.lines[row - 1])
    
    def get_word_before_cursor(self, row, col):
        if row < 0 or row >= len(self.lines):
            return ""

        line = self.lines[row][:col]

        if not line or line[-1].isspace():
            return ""

        parts = line.split()
        return parts[-1].lower() if parts else ""
