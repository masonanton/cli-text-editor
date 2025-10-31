from .base_command import Command

class NewLineCommand(Command):
    def __init__(self, row, col):
        self.row = row
        self.col = col
    
    def do(self, buffer):
        buffer.insert_newline(self.row, self.col)
        return (self.row + 1, 0)
    
    def undo(self, buffer):
        buffer.lines[self.row] += buffer.lines[self.row + 1]
        del buffer.lines[self.row + 1]
        return (self.row, self.col)

