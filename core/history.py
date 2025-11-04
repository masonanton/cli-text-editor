class History:
    def __init__(self):
        self.undo_stack = []
        self.redo_stack = []

    def record(self, command):
        self.undo_stack.append(command)
        self.redo_stack.clear()
    
    def undo(self, buffer):
        if not self.undo_stack:
            return (-1, -1)
        command = self.undo_stack.pop()
        new_row, new_col = command.undo(buffer)
        self.redo_stack.append(command)
        return new_row, new_col
    
    def redo(self, buffer):
        if not self.redo_stack:
            return (-1, -1)
        command = self.redo_stack.pop()
        new_row, new_col = command.do(buffer)
        self.undo_stack.append(command)
        return new_row, new_col
    

