from .base_key import KeyStrategy
from commands.insert_char_command import InsertCharCommand


class InsertKeyStrategy(KeyStrategy):
    def execute(self, editor, key):
        char = chr(key)
        cmd = InsertCharCommand(editor.cursor.row, editor.cursor.col, char)
        editor.cursor.update(cmd.do(editor.buffer))
        editor.history.record(cmd)

