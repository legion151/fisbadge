#!/usr/bin/python3

import data
import time
import datetime
from tkinter import *
from tkinter import simpledialog
from tkinter import messagebox 
from threading import Thread


class Gui():
    def __init__(self):
        self.members = data.Members("data.csv")
        self.g = Tk()
#        self.g.title = "Fis Badge"
        self.g.minsize(width=800,height=600)
        self.title = Label(self.g, pady=20, padx=20, font=("Arial", 24 ), text="FiS - RFID Badge Controller")
        self.title.grid(row=0, columnspan=2)
        self.resultLabel = Label(self.g,  pady=20, font=("Arial", 18), text="Person: ")
        self.resultLabel.grid(row=1, columnspan=2)



        self.createAreaTitle= Label(self.g, pady=50, font=("Arial", 20), text="Server: ")
        self.createAreaTitle.grid(row=2, columnspan=2)

        self.pullBtn = Button(self.g, text="Pull data", command=self.pullData)
        self.pullBtn.grid(row=3, column=0, sticky=E)

        self.pushBtn = Button(self.g, text="Push data", command=self.pushData)
        self.pushBtn.grid(row=3, column=1, sticky=W)


        self.createAreaTitle= Label(self.g, pady=50, font=("Arial", 20), text="Write tag: ")
        self.createAreaTitle.grid(row=4, columnspan=2)

        self.nameStr = StringVar()
        self.nameStr.trace("w", self.updateList)
        self.createAreaTitle= Label(self.g, pady=0, font=("Arial", 16), text="Filter Name: ")
        self.createAreaTitle.grid(row=5, column=0, sticky=E)
        self.nameInput = Entry(self.g,  width=20, textvariable=self.nameStr)
        self.nameInput.grid(row=5, column=1, sticky=W)

        self.forenameStr = StringVar()
        self.forenameStr.trace("w", self.updateList)
        self.createAreaTitle= Label(self.g, pady=10, font=("Arial", 16), text="Filter Vorname: ")
        self.createAreaTitle.grid(row=6, column=0, sticky=E)
        self.forenameInput = Entry(self.g, width=20, textvariable=self.forenameStr)
        self.forenameInput.grid(row=6, column=1, sticky=W)

        self.dataList = Listbox(self.g, width=80)
        self.dataList.bind("<Button-1>", lambda e : self.addBtn.configure(state="normal"))

        self.dataList.grid(row=8, columnspan=2, padx=20)


        self.showRegistered = BooleanVar()
        self.showRegistered.set(False)
        self.showRegistered.trace("w", self.updateList)
        self.checkBtn = Checkbutton(self.g, text="Zeige Registrierte", variable=self.showRegistered)
        self.checkBtn.grid(row=9, column=0, sticky=E)

        self.addBtn = Button(self.g, text="Tag schreiben",  command=self.addBtnAction, state="disabled")
        self.addBtn.grid(row=9, column=1, sticky=W)

        self.g.grid_columnconfigure(0,weight=1)
        self.g.grid_columnconfigure(1,weight=1)

        self.g.protocol('WM_DELETE_WINDOW', lambda : self.onClose())

        self.updateList()

    def updateList(self, *args):
        self.dataList.delete(0,END)

        name = self.nameStr.get()
        forename = self.forenameStr.get()
        filteredMembers = self.members.getMembersByName(name.strip(), forename.strip(), self.showRegistered.get()) 

        for member in filteredMembers:
            self.dataList.insert(END, member.ID + ": " + member.name + ", " + member.forename + "     mitgliedsstatus " + member.membertype + "     geboren " + member.birthday + "    badgecode: " + member.badgecode)



    def pullData(self):
        if messagebox.askquestion("Sure?", "Wirklich?") == 'no':
            return
        usr = simpledialog.askstring("Username", "Username")
        success = False
        if usr: 
            pwd = simpledialog.askstring("Password", "Password:", show="*")
            if usr and pwd:
               success = self.members.pullData(usr, pwd)
        if success:
            messagebox.showinfo("Success", "Success", parent=self.g)
            self.updateList()
        else:
            messagebox.showerror("Error", "Sth. went wrong!", parent=self.g)

    def pushData(self):
        if messagebox.askquestion("Sure?", "Wirklich?") == 'no':
            return
        usr = simpledialog.askstring("Username", "Username")
        success = False
        if usr: 
            pwd = simpledialog.askstring("Password", "Password:", show="*")
            if usr and pwd:
               success = self.members.pushData(usr, pwd)
        if success:
            messagebox.showinfo("Success", "Success", parent=self.g)
        else:
            messagebox.showerror("Error", "Sth. went wrong!", parent=self.g)
        

    def start(self):
        if messagebox.askquestion("Load?", "Die aktuelle Datei vom Server laden?") == 'yes':
            self.pullData()
        self.g.mainloop()

    def onClose(self):
        if messagebox.askquestion("Push?", "Die aktuellen Daten zum Server laden?") == 'yes':
            self.pushData()
        self.g.destroy()

    def showResult(self, badgecode):
        member = self.members.proofMember(badgecode)
        if not member:
            self.resultLabel.configure(text="  ACCESS DENIED  ")
            self.resultLabel.configure(bg="red")
        else:
            lastSeenStr = self.lastSeenString(member.lastseen)
            self.resultLabel.configure(text="  " + member.name + ", " + member.forename + "  mitgliedsstatus " + member.membertype + "  lastseen: " + lastSeenStr + "  ")

            if "not yet" in lastSeenStr:
                self.resultLabel.configure(bg="#00ff00")
            else:
                self.resultLabel.configure(bg="yellow")

    def lastSeenString(self, datestring):
        if datestring=="not yet": 
            return datestring
        d_last = datetime.datetime.strptime(datestring.strip(), "%Y-%m-%d %H:%M:%S")
        d_now = datetime.datetime.now()
        dif = d_now-d_last

        if(dif.days>0):
            return str(dif.days) + " days ago"
        secs = dif.seconds
        if(secs // 3600)>0:
            return str(secs//3600) + " hours ago"
        if(secs //60)>0:
            return str(secs//60) + " minutes ago"
        return str(secs) + " secs"

    def addBtnAction(self):
        if messagebox.askquestion("Sure?", "Wirklich?") == 'no':
            return
        memberID = self.dataList.get(ACTIVE).split(":")[0]
        self.members.addBadgecode(memberID, self.members.generateBadgecode())
        self.updateList()
        self.addBtn.configure(state="disabled")


def changeStuff():
    time.sleep(1)
    global gui
    gui.showResult("")
    time.sleep(3)
    mks = ["" ,"USQvwllXLIIb3UCD", "USQvwllXLIIb3UCD", "sAiTrBk679pnrwK"]
    for mk in mks:
        print("proofing: " + mk)
        gui.showResult(mk)
        time.sleep(3)



if __name__ == "__main__":
    gui = Gui()

    worker = Thread(target=changeStuff)
    worker.start()

    gui.start()
