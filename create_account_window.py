import tkinter as tk
from tkinter import messagebox

import accounts
from ui_util import center_window


class CreateAccGUI:
    """Account creation dialog. Destroyed automatically on success."""

    def cancel(self):
        self.account_window.destroy()

    def createAccount(self, event=None):
        user = self.userName_entry.get()
        pw = self.password_entry.get()
        problems = accounts.create_account(user, pw)
        if problems:
            messagebox.showerror("Cannot Create Account",
                                 "\n".join(problems),
                                 parent=self.account_window)
            self.password_entry.delete(0, tk.END)
            if accounts.username_exists(user) or accounts.validate_username(user):
                self.userName_entry.focus_set()
            else:
                self.password_entry.focus_set()
            return
        messagebox.showinfo("Account Created",
                            "Your account was created.\n"
                            "You may now log in.",
                            parent=self.account_window)
        self.created = True
        self.account_window.destroy()

    def __init__(self, parent):
        self.created = False
        self.account_window = tk.Toplevel(parent)
        win = self.account_window
        win.title("Account Creation")
        win.resizable(False, False)
        center_window(win, 500, 330)
        win.transient(parent)
        win.grab_set()
        win.columnconfigure(0, minsize=150)
        win.columnconfigure(1, minsize=300)

        tk.Label(win, text="Create an Account", font=("Georgia", 16),
                 fg="purple").grid(row=0, column=0, columnspan=2, pady=(15, 5))

        instructions = ("User name: at least 3 characters, no spaces. It must "
                        "be unique.\n\nPassword: at least nine (9) characters "
                        "and must contain at least one digit, one uppercase "
                        "letter, and one lowercase letter.")
        tk.Label(win, text=instructions, font=("Helvetica", 10),
                 wraplength=440, justify="left").grid(
                     row=1, column=0, columnspan=2, padx=20, pady=5)

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
        tk.Button(btn_frame, text=" Cancel ", width=16,
                  font=("Helvetica", 10), command=self.cancel).pack(
                      side="left", padx=10)
        tk.Button(btn_frame, text=" Create Account ", width=16,
                  font=("Helvetica", 10), command=self.createAccount).pack(
                      side="left", padx=10)

        self.userName_entry.bind("<Return>",
                                 lambda e: self.password_entry.focus_set())
        self.password_entry.bind("<Return>", self.createAccount)
        win.protocol("WM_DELETE_WINDOW", self.cancel)
        self.userName_entry.focus_set()
