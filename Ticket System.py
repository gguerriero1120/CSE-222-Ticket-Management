
import tkinter as tk              #import the tkinter module

class DataGUI:                    #declare the class
    def function1():
        print()
    def function2():
        print()
    def function3():
        print()
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
                                            command=self.function3)
        self.login_button.place(x=50,y=120)
        self.createAcc_button = tk.Button(self.main_win, text=' Create Account ',\
                                       width=16, font=("Georgia", 10),\
                                           command=self.function1)
        self.createAcc_button.place(x=200,y=120)
        self.cancel_button = tk.Button(self.main_win, text=' Cancel ',\
                                           width=16, font=("Georgia", 10),\
                                               command=self.function2)
        self.cancel_button.place(x=350,y=120)

        tk.mainloop()                                   #the main loop
                                       

dataAnalysis = DataGUI()                        #create an instance
        
