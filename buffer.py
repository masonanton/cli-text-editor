class TextBuffer:
    def __init__(self, filename = None):
        self.lines = [""]

        if filename:
            self.load_file(filename)

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