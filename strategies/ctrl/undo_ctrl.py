from .base_ctrl import CtrlKeyStrategy

class UndoCtrlKeyStrategy(CtrlKeyStrategy):
    def execute(self, editor):
        new_location = editor.history.undo(editor.buffer)
        if new_location != (-1, -1):
            editor.cursor.update(new_location)