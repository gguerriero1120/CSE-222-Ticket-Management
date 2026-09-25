import tkinter as tk

class CreateAccGUI:
    def cancel(acct):
        acct.account_window.destroy()
    def createAccount(acct):
        print()
    def __init__(acct):
        acct.account_window = tk.Tk()
        acct.account_window.title("Account Creation")
        acct.account_window.minsize(width=500,height=350)

        acct.account_window.columnconfigure(0, minsize = 150)
        acct.account_window.columnconfigure(1, minsize = 175)

        acct.account_window.rowconfigure(0, minsize = 50)
        acct.account_window.rowconfigure(1, minsize = 50)
        acct.account_window.rowconfigure(2, minsize = 50)
        acct.account_window.rowconfigure(3, minsize = 50)
        
        acct.heading_label=tk.Label(acct.account_window, text='User name:',\
                                    font=("Helevetica",10))
        acct.heading_label.grid(row=0, column=0)

        acct.heading_label=tk.Label(acct.account_window, text='Create a password of at least nine(9) characters, that contain at least one digit, one uppercase, and one lowercase letter.',\
                                    font=("Helevetica",10))
        acct.heading_label.grid(row=1, column=1)

        acct.heading_label=tk.Label(acct.account_window, text='Password:',\
                                    font=("Helevetica",10))
        acct.heading_label.grid(row=2, column=0)

        acct.cancel_button = tk.Button(acct.account_window, text=' Cancel ',\
                                       width=16, font=("Helevetica",10),\
                                           command=acct.cancel)
        acct.cancel_button.grid(row=3, column=0)

        acct.createAccount_button = tk.Button(acct.account_window, text=' Create Account ',\
                                              width=16, font=("Helevetica",10),\
                                              command=acct.createAccount)
        acct.createAccount_button.grid(row=3, column=1)
                                       

        acct.account_window.userName_entry=tk.Entry(acct.account_window,\
                                                         width=15, justify='right', font=("Helvetica", 10))
        acct.account_window.userName_entry.grid(row=0, column=1, sticky='W')
        acct.account_window.userName_entry.focus_force()
        
        acct.account_window.userName_entry=tk.Entry(acct.account_window,\
                                                         width=15, justify='right', font=("Helvetica", 10))
        acct.account_window.userName_entry.grid(row=2, column=1, sticky='W')
        acct.account_window.userName_entry.focus_force()

        tk.mainloop()
