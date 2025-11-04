# CLI Text Editor

This is a simple command-line text editor built in Python using the `curses` library. It's meant to simulate a lightweight, extensible editing environment — something that feels like a stripped-down version of Vim or Nano, but implemented from scratch. The editor supports cursor movement, text insertion and deletion, undo/redo, file saving/loading, and a command-based architecture designed for easy feature expansion.

## How to Run

From the project root, run:
```bash
python editor.py <filename>
```

If the file doesn't exist, the editor will create it.

## Controls

### Basic Movement

- **Arrow Keys** — Move the cursor up, down, left, and right
- **Home / End** — Jump to the start or end of the current line
- **Page Up / Page Down** — Move up or down one screen's worth of lines

### Editing

- **Character keys** — Insert text at the cursor position
- **Backspace** — Delete the character before the cursor
- **Delete** — Delete the character at the cursor
- **Enter** — Insert a new line below the current one

### File Commands

- **Ctrl + S** — Save the current buffer to the file
- **Ctrl + Q** — Quit the editor

### Undo / Redo

- **Ctrl + Z** — Undo the last operation
- **Ctrl + Y** — Redo the most recently undone operation

## Architecture Overview

The editor is built around three main concepts:

- **Buffer** — Stores the text lines and handles insert/delete operations
- **Cursor** — Tracks the current position and updates dynamically
- **History** — Implements undo/redo using the Command pattern

Each keystroke is handled by a `KeyStrategy`, and each edit action (insert, delete, newline, etc.) is encapsulated in a `Command` object that can be executed or undone.

---

This project is mostly an experiment in design patterns and terminal UI handling, rather than a full-fledged text editor — but it provides a clean, extensible base to build on.
