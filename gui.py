#!/usr/bin/python3

import data
import time
import datetime
import sound
from tkinter import *
from tkinter import simpledialog
from tkinter import messagebox 
from threading import Thread
import arduCon#_stub as arduCon

def dbg(s, err=""):
    if(len(err)>0):
        print(f"gui: {s} err:{err}")
    else:
        print(f"gui: {s}")

def getUserCreds():
    try:
        with open("creds") as f:
            lines = f.readlines()
            lines = list(filter(lambda e: e , lines))
            lines = list(filter(lambda e: not e.startswith("#"), lines))
            usr = lines[0].split(":")[1].strip()
            pwd = lines[1].split(":")[1].strip()
            if usr and pwd:
                return (usr, pwd)
    except:
        pass
    
    usr = simpledialog.askstring("Username", "Username")
    if usr:
        pwd = simpledialog.askstring("Password", "Password:", show="*")
        if usr and pwd:
            return (usr, pwd)
    return None


class Gui():
    def __init__(self):
        self.sound = sound.Sound()
        self.arduCon = arduCon.Ardu()
        self.badgeWasThere = False
        self.members = data.Members("data.csv")
        self.g = Tk()
        self.g.iconbitmap("./logo_fis.ico")
        self.g.title("FiS - RFID Badge Controller")
        self.g.minsize(width=800,height=400)
        Label(self.g, pady=20, padx=20, font=("Arial", 22 ), text="FiS - RFID Badge Controller").grid(row=0, columnspan=2)

        self.resultLabel = Label(self.g,  pady=15, font=("Arial", 16), text="Person: ")
        self.resultLabel.grid(row=1, columnspan=2)

        Label(self.g, pady=30, font=("Arial", 16), text="Server: ").grid(row=2, columnspan=2)

        Button(self.g, text="Pull data", command=self.pullData).grid(row=3, column=0, sticky=E)
        Button(self.g, text="Push data", command=self.pushData).grid(row=3, column=1, sticky=W)


        Label(self.g, pady=30, font=("Arial", 16), text="Write tag: ").grid(row=4, columnspan=2)

        self.nameStr = StringVar()
        self.nameStr.trace("w", self.updateList)
        Label(self.g, pady=0, font=("Arial", 14), text="Filter surname: ").grid(row=5, column=0, sticky=E)
        Entry(self.g,  width=20, textvariable=self.nameStr).grid(row=5, column=1, sticky=W)

        self.forenameStr = StringVar()
        self.forenameStr.trace("w", self.updateList)
        Label(self.g, pady=10, font=("Arial", 14), text="Filter forename: ").grid(row=6, column=0, sticky=E)
        Entry(self.g, width=20, textvariable=self.forenameStr).grid(row=6, column=1, sticky=W)

        self.dataList = Listbox(self.g, width=80)
        self.dataList.grid(row=8, columnspan=2, padx=20)


        self.showRegistered = BooleanVar()
        self.showRegistered.set(False)
        self.showRegistered.trace("w", self.updateList)
        Checkbutton(self.g, text="Show registered", variable=self.showRegistered).grid(row=9, column=0, sticky=E)

        self.addBtn = Button(self.g, text="Write to badge",  command=self.addBtnAction, state="disabled")
        self.addBtn.grid(row=9, column=1, sticky=W)

        self.connectedLabel = Label(self.g, text="connected", bg="red", pady=5, padx=5)
        self.connectedLabel.grid(row=9, column=1)

        self.g.grid_columnconfigure(0,weight=1)
        self.g.grid_columnconfigure(1,weight=1)
        self.g.protocol('WM_DELETE_WINDOW', lambda : self.onClose())


        self.updateList()
        self.showResult()
        self.guiLoop()

    def writeBtnAvailability(self):
        if(self.dataList.get(ACTIVE) and self.badgeWasThere):
            self.addBtn.configure(state="normal")
        else:
            self.addBtn.configure(state="disabled")

    def showConnected(self, b):
        if(b):
            self.connectedLabel.configure(text="connected", bg="#00ff00")
        else:
            self.connectedLabel.configure(text="no rfid", bg="red")
    

    def updateList(self, *args):
        self.dataList.delete(0,END)

        name = self.nameStr.get()
        forename = self.forenameStr.get()
        filteredMembers = self.members.getMembersByName(name.strip(), forename.strip(), self.showRegistered.get()) 

        for member in filteredMembers:
            self.dataList.insert(END, member.ID + ": " + member.name + ", " + member.forename + "     memberstate " + member.membertype + "     birth " + member.birthday + "    badgecode: " + member.badgecode)


    def pullData(self):
        if messagebox.askquestion("Sure?", "Sure?") == 'no':
            return
        creds = getUserCreds()
        if creds:
            if self.members.pullData(creds[0], creds[1]):
                messagebox.showinfo("Success", "Success", parent=self.g)
                self.updateList()
                return 
        messagebox.showerror("Error", "Sth. went wrong!", parent=self.g)

    def pushData(self):
        if messagebox.askquestion("Sure?", "Sure?") == 'no':
            return
        creds = getUserCreds()
        if creds:
            if self.members.pushData(creds[0], creds[1]):
                messagebox.showinfo("Success", "Success", parent=self.g)
                return 
        messagebox.showerror("Error", "Sth. went wrong!", parent=self.g)
       
    def start(self):
        if messagebox.askquestion("Load?", "Load data from server?") == 'yes':
            self.pullData()
        self.g.mainloop()

    def onClose(self):
        if messagebox.askquestion("Push?", "Push data to server?") == 'yes':
            self.pushData()
        self.g.destroy()

    def guiLoop(self):
        #pingpong will corrupt states so don't do it
        if(not self.badgeWasThere):
            if(self.arduCon.connect()):
                self.showConnected(True)
            else:
                self.showConnected(False)

        self.badgeWasThere = self.showResult()
        dbg(f"badgeWasThere: {self.badgeWasThere }")
        self.writeBtnAvailability()

        self.g.after(500, self.guiLoop)


    def showResult(self):
        scannedBadge = self.arduCon.readTag()

        dbg(f"scannedbadge: {scannedBadge}")
        if(scannedBadge):
            l = len(scannedBadge)
            dbg(f"len of code: {l}")
        if scannedBadge and len(scannedBadge)==16:
            #don't update gui and file and stuff on every cycle but detect if removed - needs rework 
            if(self.badgeWasThere == scannedBadge):
                return scannedBadge
            dbg(f"scannedBadge: {scannedBadge}")
            member = self.members.proofMember(scannedBadge)
            if not member:
                self.resultLabel.configure(text="  ACCESS DENIED  ")
                self.resultLabel.configure(bg="red")
                self.sound.bad()
                return scannedBadge
            else:
                lastSeenStr = self.lastSeenString(member.lastseen)
                self.resultLabel.configure(text="  " + member.name + ", " + member.forename + "  memberstate " + member.membertype + "  lastseen: " + lastSeenStr + "  ")
    
                if "not yet" in lastSeenStr:
                    self.resultLabel.configure(bg="#00ff00")
                else:
                    self.resultLabel.configure(bg="yellow")
                self.sound.good()
                return scannedBadge
        return False
        

    def lastSeenString(self, datestring):
        if datestring=="not yet": 
            return datestring
        d_last = datetime.datetime.strptime(datestring.strip(), "%Y-%m-%d %H:%M:%S")
        d_now = datetime.datetime.now()
        dif = d_now-d_last
        dbg(datestring)

        if(dif.days>0):
            return str(dif.days) + " days ago"
        secs = dif.seconds
        if(secs // 3600)>0:
            return str(secs//3600) + " hours ago"
        if(secs //60)>0:
            return str(secs//60) + " minutes ago"
        return str(secs) + " secs"

    def addBtnAction(self):
        if messagebox.askquestion("Sure?", "Sure?") == 'no':
            return
        memberID = self.dataList.get(ACTIVE).split(":")[0]
        genCode = self.members.generateBadgecode()
        self.arduCon.writeTag(genCode)
        self.members.addBadgecode(memberID, genCode)
        self.updateList()


if __name__ == "__main__":
    Gui().start()



