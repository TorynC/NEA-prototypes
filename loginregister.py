import sqlite3
from tkinter import *

#setup database connection and create table
with sqlite3.connect("Data.db") as db:
    cursor = db.cursor()
cursor.execute(""" CREATE TABLE IF NOT EXISTS CustomerDetails(
UserID integer PRIMARY KEY, 
Username TEXT NOT NULL,
Password TEXT NOT NULL,
TutorGroup TEXT); 
""")
cursor.execute(""" CREATE TABLE IF NOT EXISTS TotalTimes(
ID integer PRIMARY KEY,
Time INTEGER);
""")
cursor.execute(""" CREATE TABLE IF NOT EXISTS 
LoggedIn(AttemptID integer PRIMARY KEY,
Username TEXT NOT NULL,
Password TEXT NOT NULL,
TutorGroup TEXT,
Score INTEGER,
Time INTEGER);
""")
db.commit()
db.close()

#master parameter means main window
class Main:
    def __init__(self,master):
        self.master=master
        self.master.title("Grave Fighter")
        self.master.geometry("600x600")

        #for textvariable
        self.username=StringVar()
        self.password = StringVar()
        self.tutorgroup = StringVar()
        self.new_username = StringVar()
        self.new_password = StringVar()
        self.new_tutorgroup = StringVar()

        self.menu_widgets()

    def menu_widgets(self):
        for i in self.master.winfo_children():
            i.destroy()
        self.frame = Frame(self.master)
        self.title = Label(self.master,text = "Main Menu",font=('',50))
        self.title.pack(pady=10)
        self.button1 = Button(self.frame,text = "Login",font=("",20),command=self.login)
        self.button2 = Button(self.frame,text = "Create New Account",font=("",20),command=self.create_acc)
        self.button3 = Button(self.frame,text="Quit",font=("",20),command=self.quit)
        self.frame.pack()
        self.button1.pack(padx=10,pady=15)
        self.button2.pack(padx=10,pady=20)
        self.button3.pack(padx=10,pady=25)

    def create_acc(self):
        for i in self.master.winfo_children():
            i.destroy()

        self.new_username.set('')
        self.new_password.set('')
        self.new_tutorgroup.set('')

        self.register_frame = Frame(self.master).grid(row=0,column=0)
        self.title2 = Label(self.register_frame,text="Create New Account",font=('',30)).grid(row=1,column=1)
        self.n_usernamelabel = Label(self.register_frame,text="New Username:",font = 20).grid(row=7,column=0)
        self.n_passwordlabel = Label(self.register_frame,text = "New Password:",font = 20).grid(row=8,column=0)
        self.n_tutorgrouplabel = Label(self.register_frame,text = "Tutor Group:",font=20).grid(row=9,column=0)
        self.n_usernameentry = Entry(self.register_frame,textvariable=self.new_username).grid(row=7,column=1)
        self.n_passwordentry =Entry(self.register_frame,textvariable=self.new_password).grid(row=8,column=1)
        self.n_tutorgroup = Entry(self.register_frame,textvariable = self.new_tutorgroup).grid(row=9,column=1)
        self.createaccbutt= Button(self.register_frame,text="Create Account",command=self.newacc).grid(row=11,column=1)
        self.loginbutt = Button(self.register_frame,text="Login Page",command=self.login).grid(row=12,column=1)
        self.menubutt = Button(self.register_frame,text="Back to Main Menu",command=self.menu_widgets).grid(row=13,column=1)

    def login(self):
        for i in self.master.winfo_children():
            i.destroy()
        self.username.set('')
        self.password.set('')
        self.tutorgroup.set('')

        self.login_frame = Frame(self.master).grid(row=0,column=0)
        self.title3 = Label(self.login_frame,text = "Login", font = ('',30)).grid(row=1,column=0)
        self.lognamelabel = Label(self.login_frame,text="Username:",font=20).grid(row=3,column=0)
        self.logpasslabel = Label(self.login_frame,text="Password:",font=20).grid(row=4,column=0)
        self.logtutorlabel = Label(self.login_frame,text = "Tutor Group:",font=20).grid(row=5,column=0)
        self.lognameentry = Entry(self.login_frame,textvariable=self.username).grid(row=3,column=1)
        self.logpassentry = Entry(self.login_frame,textvariable= self.password,show="*").grid(row=4,column=1)
        self.logtutorentry = Entry(self.login_frame,textvariable=self.tutorgroup).grid(row=5,column=1)
        self.menu2butt = Button(self.login_frame,text = "Back to Main Menu",command = self.menu_widgets).grid(row=7,column=1)
        self.login2butt = Button(self.login_frame,text = "Login",command = self.oldacc).grid(row=6,column=1)

    def newacc(self):
        with sqlite3.connect("Data.db") as db:
            cursor1 = db.cursor()
        find_user = ("SELECT Username FROM CustomerDetails WHERE Username = ? ")
        cursor1.execute(find_user,[(self.new_username.get())])
        self.message = Label(self.register_frame)
        self.message.grid(row=14,column=1)
        if cursor1.fetchall():
            self.message.config(text="Username taken, Try a different one.")
        elif self.new_username.get() == "" or self.new_password.get() == "" or self.new_tutorgroup.get() == "":
            self.message.config(text = "         Cannot have empty entry        ")
        else:
            self.message.config(text="                 Account Created!                   ")
            insert = 'INSERT INTO CustomerDetails(Username,Password,TutorGroup) VALUES(?,?,?)'
            cursor1.execute(insert,[(self.new_username.get()),(self.new_password.get()),(self.new_tutorgroup.get())])
            db.commit()

    def oldacc(self):
        with sqlite3.connect("Data.db") as db:
            cursor2 = db.cursor()
            cursor2.execute("SELECT * FROM CustomerDetails WHERE Username = ? AND Password = ? AND TutorGroup=?",(self.username.get(),self.password.get(),self.tutorgroup.get()))
            row = cursor2.fetchall()
            db.commit()
        if row !=[]:
            cursor2.execute('INSERT INTO LoggedIn(Username,Password,TutorGroup) VALUES(?,?,?)',[self.username.get(),self.password.get(),self.tutorgroup.get()])
            db.commit()
            window1.destroy()
            import game

        else:
            self.message2 = Label(self.login_frame,text="User not found.").grid(row=8,column=1)

    def quit(self):
        window1.destroy()

window1 = Tk()
b = Main(window1)
window1.mainloop()
