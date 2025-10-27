class TextBuffer:
    def __init__(self):
        # TODO: load a provided file
        self.lines = [
            "Hello, world!",
            "This is a test.",
            "Cursor movement check.",
            "Short",
            "A much longer line to test bounds",
        ]

    # TODO: add/insert operations 