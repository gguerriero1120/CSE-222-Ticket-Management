import tkinter as tk
from tkinter import messagebox

import accounts
from ui_util import center_window


class LoginGUI:
    """Login dialog.

    on_success() is called after a good login; on_cancel() if the user
    closes/cancels the dialog. Both are supplied by the main GUI.
    """

    def cancel(self):
        self.login_window.destroy()
        if self.on_cancel:
            self.on_cancel()

    def verify(self, event=None):
        """Bound to <Return> in the entry controls and used by the button."""
        user = self.userName_entry.get()
        pw = self.password_entry.get()
        if user.strip() and pw and accounts.verify(user, pw):
            self.login_window.destroy()
            if self.on_success:
                self.on_success(user.strip())
        else:
            messagebox.showerror("Login Failed",
                                 "The user name or password is incorrect.",
                                 parent=self.login_window)
            self.userName_entry.delete(0, tk.END)
            self.password_entry.delete(0, tk.END)
            self.userName_entry.focus_set()

    def login(self):
        self.verify()

    def __init__(self, parent, on_success=None, on_cancel=None):
        self.on_success = on_success
        self.on_cancel = on_cancel
        self.login_window = tk.Toplevel(parent)
        win = self.login_window
        win.title("Login")
        win.resizable(False, False)
        center_window(win, 450, 280)
        win.transient(parent)
        win.grab_set()
        win.columnconfigure(0, minsize=140)
        win.columnconfigure(1, minsize=280)

        tk.Label(win, text="Account Login", font=("Georgia", 16),
                 fg="purple").grid(row=0, column=0, columnspan=2, pady=(20, 5))
        tk.Label(win, text="Enter your user name and password, then press "
                           "<Enter> or click Login.",
                 font=("Helvetica", 9), wraplength=400).grid(
                     row=1, column=0, columnspan=2, pady=5)

        tk.Label(win, text="User name:", font=("Helvetica", 10)).grid(
            row=2, column=0, sticky="E", padx=10, pady=8)
        self.userName_entry = tk.Entry(win, width=22, justify="right",
                                       font=("Helvetica", 10))
        self.userName_entry.grid(row=2, column=1, sticky="W")

        tk.Label(win, text="Password:", font=("Helvetica", 10)).grid(
            row=3, column=0, sticky="E", padx=10, pady=8)
        self.password_entry = tk.Entry(win, width=22, justify="right",
                                       show="*", font=("Helvetica", 10))
        self.password_entry.grid(row=3, column=1, sticky="W")

        btn_frame = tk.Frame(win)
        btn_frame.grid(row=4, column=0, columnspan=2, pady=20)
        tk.Button(btn_frame, text=" Cancel ", width=14,
                  font=("Helvetica", 10), command=self.cancel).pack(
                      side="left", padx=10)
        tk.Button(btn_frame, text=" Login ", width=14,
                  font=("Helvetica", 10), command=self.login).pack(
                      side="left", padx=10)

        # <Enter> key handling
        self.userName_entry.bind("<Return>",
                                 lambda e: self.password_entry.focus_set())
        self.password_entry.bind("<Return>", self.verify)
        win.protocol("WM_DELETE_WINDOW", self.cancel)
        self.userName_entry.focus_set()
