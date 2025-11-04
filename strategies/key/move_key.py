from .base_key import KeyStrategy

class MoveKeyStrategy():
    def execute(self, editor, key):
        editor.cursor.move(key, editor.buffer)