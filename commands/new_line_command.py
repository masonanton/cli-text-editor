from .base_command import Command

def NewLineCommand(Commmand):
    def __init__(self, row, col):
        self.row = row
        self.col = col
    
    def do(self, buffer):
        buffer.insert_newline(self.row, self.col)
    
    def undo(self, buffer):
        buffer.lines[self.row] += buffer.lines[self.row + 1]
        del buffer.lines[self.row + 1]

