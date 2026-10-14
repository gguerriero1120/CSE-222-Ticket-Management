"""Small shared GUI helpers."""


def center_window(win, width, height):
    """Size a window and place it in the center of the desktop."""
    win.update_idletasks()
    x = (win.winfo_screenwidth() - width) // 2
    y = (win.winfo_screenheight() - height) // 2
    win.geometry(f"{width}x{height}+{x}+{max(y, 0)}")
