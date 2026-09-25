import tkinter as tk

class LoginGUI:
    def cancel(acct):
        acct.login_window.destroy()
    def login(acct):
        print()
    def __init__(acct):
        acct.login_window = tk.Tk()
        acct.login_window.title("Login")
        acct.login_window.minsize(width=500,height=350)

        acct.login_window.columnconfigure(0, minsize = 150)
        acct.login_window.columnconfigure(1, minsize = 150)
        acct.login_window.columnconfigure(1, minsize = 150)
        
        acct.login_window.rowconfigure(0, minsize = 50)
        acct.login_window.rowconfigure(1, minsize = 50)
        acct.login_window.rowconfigure(2, minsize = 50)
        acct.login_window.rowconfigure(3, minsize = 50)

        acct.heading_label=tk.Label(acct.login_window, text='Account Login',\
                                    font=("Helevetica",16))
        acct.heading_label.grid(row=0, column=1)
        
        acct.heading_label=tk.Label(acct.login_window, text='User name:',\
                                    font=("Helevetica",10))
        acct.heading_label.grid(row=1, column=0)

        acct.heading_label=tk.Label(acct.login_window, text='Password:',\
                                    font=("Helevetica",10))
        acct.heading_label.grid(row=2, column=0)

        acct.cancel_button = tk.Button(acct.login_window, text=' Cancel ',\
                                       width=16, font=("Helevetica",10),\
                                           command=acct.cancel)
        acct.cancel_button.grid(row=3, column=0)

        acct.login_button = tk.Button(acct.login_window, text=' Login ',\
                                              width=16, font=("Helevetica",10),\
                                              command=acct.login)
        acct.login_button.grid(row=3, column=2)
                                       

        acct.login_window.userName_entry=tk.Entry(acct.login_window,\
                                                         width=15, justify='right', font=("Helvetica", 10))
        acct.login_window.userName_entry.grid(row=1, column=1, sticky='W')
        acct.login_window.userName_entry.focus_force()
        
        acct.login_window.userName_entry=tk.Entry(acct.login_window,\
                                                         width=15, justify='right', font=("Helvetica", 10))
        acct.login_window.userName_entry.grid(row=2, column=1, sticky='W')
        acct.login_window.userName_entry.focus_force()

        tk.mainloop()
