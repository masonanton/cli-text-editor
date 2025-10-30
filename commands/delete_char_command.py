from .base_command import Command

def DeleteCharCommand(Command):
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.deleted_char = None
    
    def do(self, buffer):
        buffer.delete_char(self.row, self.col)

    def undo(self, buffer):
        if not self.deleted_char:
            return
        buffer.insert_char(self.row, self.col, self.deleted_char)
