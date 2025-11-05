from .base_command import Command

class InsertCharCommand(Command):
    def __init__(self, row, col, char):
        self.row = row
        self.col = col
        self.char = char    

    def do(self, buffer):
        overflow = buffer.insert_char(self.row, self.col, self.char)
        return (self.row, self.col + 1) if overflow == 0 else (self.row + 1, overflow)

    def undo(self, buffer):
        buffer.delete_char(self.row, self.col + 1)
        return (self.row, self.col)



