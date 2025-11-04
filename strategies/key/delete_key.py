from .base_key import KeyStrategy
from commands.delete_char_command import DeleteCharCommand

class DeleteKeyStrategy(KeyStrategy):
    def execute(self, editor):
        if editor.cursor.col == 0 and editor.cursor.row == 0:
            return
        cmd = DeleteCharCommand(editor.cursor.row, editor.cursor.col)
        editor.cursor.update(cmd.do(editor.buffer))
        editor.history.record(cmd)
