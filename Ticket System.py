
import tkinter as tk              #import the tkinter module
import data_create_acct
import data_login

class DataGUI:                    #declare the class
    def create_account(self):
        createAcctWin = data_create_acct.CreateAccGUI()
        createAcctWin.account_window.wait_window()
        self.createAcc_button.config(state='disabled')
        self.login_button.config(state='normal')

    def login(self):
        loginWin = data_login.LoginGUI()
        loginWin.login_window.wait_window()
        
    def cancel(self):
        self.main_win.destroy()
        
    def __init__(self):         #initialization function
        self.main_win = tk.Tk()   #create main window 
        self.main_win.title("Theater Ticket System")    #title bar label
        self.main_win.minsize(width=550,height=200)     #window size
        self.main_win.columnconfigure(0, minsize = 150)
        self.main_win.columnconfigure(1, minsize = 175)
        self.main_win.columnconfigure(2, minsize = 150)
        self.main_win.rowconfigure(0, minsize = 50)
        
        self.heading_label=tk.Label(text='Theater Ticket System',\
                                    font=("Georgia",16),fg="purple")
        self.heading_label.grid(row=2,column=1)         #label location

        self.login_button = tk.Button(self.main_win, text=' Login ',\
                                       width=16, font=("Georgia", 10),\
                                            command=self.login)
        self.login_button.place(x=50,y=120)
        
        self.createAcc_button = tk.Button(self.main_win, text=' Create Account ',\
                                       width=16, font=("Georgia", 10),\
                                           command=self.create_account)
        self.createAcc_button.place(x=200,y=120)
        
        self.cancel_button = tk.Button(self.main_win, text=' Cancel ',\
                                           width=16, font=("Georgia", 10),\
                                               command=self.cancel)
        self.cancel_button.place(x=350,y=120)

        tk.mainloop()                                   #the main loop
                                       

dataAnalysis = DataGUI()                        #create an instance
        
        
        
