from .base_ctrl import CtrlKeyStrategy

class RedoCtrlKeyStrategy(CtrlKeyStrategy):
    def execute(self, editor):
        new_location = editor.history.redo(editor.buffer)
        if new_location != (-1, -1):
            editor.cursor.update(new_location)