from .base_command import Command

class InsertCharCommand(Command):
    def __init__(self, row, col, char):
        self.row = row
        self.col = col
        self.char = char    

    def do(self, buffer):
        buffer.insert_char(self.row, self.col, self.char)

    def undo(self, buffer):
        buffer.delete_char(self.row, self.col)



