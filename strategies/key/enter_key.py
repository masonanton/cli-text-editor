from .base_key import KeyStrategy
from commands.new_line_command import NewLineCommand

class EnterKeyStrategy(KeyStrategy):
    def execute(self, editor):
        cmd = NewLineCommand(editor.cursor.row, editor.cursor.col)
        editor.cursor.update(cmd.do(editor.buffer))
        editor.history.record(cmd)
