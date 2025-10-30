class Command:
    def do(self, buffer):
        raise NotImplementedError

    def undo(self, buffer):
        raise NotImplementedError