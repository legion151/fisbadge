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
        self.resultLabel = Label(self.g, pady=20, font=("Arial", 18), text="Person: ")
        self.resultLabel.grid(row=1, columnspan=2)



        self.createAreaTitle= Label(self.g, pady=50, font=("Arial", 20), text="Server: ")
        self.createAreaTitle.grid(row=2, columnspan=2)

        self.pullBtn = Button(self.g, text="Pull data", command=self.pullData)
        self.pullBtn.grid(row=3, column=0, sticky=E)

        self.pushBtn = Button(self.g, text="Push data", command=self.pushData)
        self.pushBtn.grid(row=3, column=1, sticky=W)


        self.createAreaTitle= Label(self.g, pady=50, font=("Arial", 20), text="Write tag: ")
        self.createAreaTitle.grid(row=4, columnspan=2)

        self.createAreaTitle= Label(self.g, pady=0, font=("Arial", 16), text="Filter Name: ")
        self.createAreaTitle.grid(row=5, column=0, sticky=E)
        self.nameInput = Entry(self.g,  width=20)
        self.nameInput.grid(row=5, column=1, sticky=W)
        self.nameInput.bind("<Key>", self.updateList)

        self.createAreaTitle= Label(self.g, pady=10, font=("Arial", 16), text="Filter Vorname: ")
        self.createAreaTitle.grid(row=6, column=0, sticky=E)
        self.forenameInput = Entry(self.g, width=20)
        self.forenameInput.bind("<Key>", self.updateList)
        self.forenameInput.grid(row=6, column=1, sticky=W)

        self.dataList = Listbox(self.g, width=80)
        self.dataList.bind("<Button-1>", lambda e : self.addBtn.configure(state="normal"))

        self.updateList(None)
        self.dataList.grid(row=8, columnspan=2, padx=20)

        self.addBtn = Button(self.g, text="Tag schreiben",  command=self.addBtnAction, state="disabled")
        self.addBtn.grid(row=9, columnspan=2)

    def pullData(self):
        usr = simpledialog.askstring("Username", "Username")
        success = False
        if usr: 
            pwd = simpledialog.askstring("Password", "Password:")
            if usr and pwd:
               success = self.members.pullData(usr, pwd)
        if success:
            messagebox.showinfo("Success", "Success", parent=self.g)
        else:
            messagebox.showerror("Error", "Sth. went wrong!", parent=self.g)

    def pushData(self):
        usr = simpledialog.askstring("Username", "Username")
        success = False
        if usr: 
            pwd = simpledialog.askstring("Password", "Password:")
            if usr and pwd:
               success = self.members.pushData(usr, pwd)
        if success:
            messagebox.showinfo("Success", "Success", parent=self.g)
        else:
            messagebox.showerror("Error", "Sth. went wrong!", parent=self.g)
        

    def start(self):
        self.g.mainloop()

    def showResult(self, badgecode):
        member = self.members.proofMember(badgecode)
        if not member:
            self.resultLabel.configure(text=" ACCESS DENIED ")
            self.resultLabel.configure(bg="red")
        else:
            lastSeenStr = self.lastSeenString(member.lastseen)
            self.resultLabel.configure(text=" " + member.name + ", " + member.forename + "  mitgliedsstatus " + member.membertype + "  lastseen: " + lastSeenStr)

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
        self.updateList(None)
        self.addBtn.configure(state="disabled")


    def updateList(self, eve):
        self.dataList.delete(0,END)
        name = self.nameInput.get()
        forename = self.forenameInput.get()
        filteredMembers = self.members.getMembersByName(name, forename) 

        for member in filteredMembers:
            self.dataList.insert(END, member.ID + ": " + member.name + ", " + member.forename + "     mitgliedsstatus " + member.membertype + "     geboren " + member.birthday)



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
