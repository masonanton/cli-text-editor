from .base_ctrl import CtrlKeyStrategy

class SaveCtrlKeyStrategy(CtrlKeyStrategy):
    def execute(self, editor):
        if not editor.filename:
            editor.filename = editor.prompt_filename("Save as: ")
            if not editor.filename:
                return
        editor.buffer.save_file(editor.filename)
        max_y, _ = editor.stdscr.getmaxyx()
        editor.stdscr.addstr(max_y - 1, 0, f"Saved to {editor.filename}".ljust(60))
        editor.stdscr.refresh()