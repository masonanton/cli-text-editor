from .base_command import Command

class DeleteCharCommand(Command):
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.deleted_char = None
    
    def do(self, buffer):
        self.deleted_char = buffer.delete_char(self.row, self.col)
        if self.deleted_char is None:
            return (self.row, self.col)

        if self.deleted_char == "\n":
            return (self.row - 1, len(buffer.lines[self.row - 1]) if self.row > 0 else 0)
        else:
            return (self.row, self.col - 1)

    def undo(self, buffer):
        if self.deleted_char:
            if self.deleted_char == "\n":
                buffer.insert_newline(self.row - 1, self.col)
            else:
                buffer.insert_char(self.row, self.col - 1, self.deleted_char)
        return (self.row, self.col)