class History:
    def __init__(self):
        self.undo_stack = []
        self.redo_stack = []

    def record(self, command):
        self.undo_stack.append(command)
        self.redo_stack.clear()
    
    def undo(self, buffer):
        if not self.undo_stack:
            return
        command = self.undo_stack.pop()
        command.undo(buffer)
        self.redo_stack.append(command)
    
    def redo(self, buffer):
        if not self.redo_stack:
            return
        command = self.redo_stack.pop()
        command.do(buffer)
        self.undo_stack.append(command)
    

