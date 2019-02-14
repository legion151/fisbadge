#!/usr/bin/python3

import data
import time
import datetime
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
        self.arduCon = arduCon.Ardu()
        self.badgeWasThere = False
        self.members = data.Members("data.csv")
        self.g = Tk()
        self.g.minsize(width=800,height=600)
        Label(self.g, pady=20, padx=20, font=("Arial", 24 ), text="FiS - RFID Badge Controller").grid(row=0, columnspan=2)

        self.resultLabel = Label(self.g,  pady=20, font=("Arial", 18), text="Person: ")
        self.resultLabel.grid(row=1, columnspan=2)

        Label(self.g, pady=50, font=("Arial", 20), text="Server: ").grid(row=2, columnspan=2)

        Button(self.g, text="Pull data", command=self.pullData).grid(row=3, column=0, sticky=E)
        Button(self.g, text="Push data", command=self.pushData).grid(row=3, column=1, sticky=W)


        Label(self.g, pady=50, font=("Arial", 20), text="Write tag: ").grid(row=4, columnspan=2)

        self.nameStr = StringVar()
        self.nameStr.trace("w", self.updateList)
        Label(self.g, pady=0, font=("Arial", 16), text="Filter Name: ").grid(row=5, column=0, sticky=E)
        Entry(self.g,  width=20, textvariable=self.nameStr).grid(row=5, column=1, sticky=W)

        self.forenameStr = StringVar()
        self.forenameStr.trace("w", self.updateList)
        Label(self.g, pady=10, font=("Arial", 16), text="Filter Vorname: ").grid(row=6, column=0, sticky=E)
        Entry(self.g, width=20, textvariable=self.forenameStr).grid(row=6, column=1, sticky=W)

        self.dataList = Listbox(self.g, width=80)
        self.dataList.grid(row=8, columnspan=2, padx=20)


        self.showRegistered = BooleanVar()
        self.showRegistered.set(False)
        self.showRegistered.trace("w", self.updateList)
        Checkbutton(self.g, text="Zeige Registrierte", variable=self.showRegistered).grid(row=9, column=0, sticky=E)

        self.addBtn = Button(self.g, text="Tag schreiben",  command=self.addBtnAction, state="disabled")
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
            self.dataList.insert(END, member.ID + ": " + member.name + ", " + member.forename + "     mitgliedsstatus " + member.membertype + "     geboren " + member.birthday + "    badgecode: " + member.badgecode)


    def pullData(self):
        if messagebox.askquestion("Sure?", "Wirklich?") == 'no':
            return
        creds = getUserCreds()
        if creds:
            if self.members.pullData(creds[0], creds[1]):
                messagebox.showinfo("Success", "Success", parent=self.g)
                self.updateList()
                return 
        messagebox.showerror("Error", "Sth. went wrong!", parent=self.g)

    def pushData(self):
        if messagebox.askquestion("Sure?", "Wirklich?") == 'no':
            return
        creds = getUserCreds()
        if creds:
            if self.members.pushData(creds[0], creds[1]):
                messagebox.showinfo("Success", "Success", parent=self.g)
                return 
        messagebox.showerror("Error", "Sth. went wrong!", parent=self.g)
       
    def start(self):
        if messagebox.askquestion("Load?", "Die aktuelle Datei vom Server laden?") == 'yes':
            self.pullData()
        self.g.mainloop()

    def onClose(self):
        if messagebox.askquestion("Push?", "Die aktuellen Daten zum Server laden?") == 'yes':
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
        self.writeBtnAvailability()

        self.g.after(200, self.guiLoop)


    def showResult(self):
        scannedBadge = self.arduCon.read()
        if scannedBadge and len(scannedBadge)==16:
            #don't update gui and file and stuff on every cycle but detect if removed - needs rework 
            if(self.badgeWasThere):
                return True
            dbg(f"scannedBadge: {scannedBadge}")
            member = self.members.proofMember(scannedBadge)
            if not member:
                self.resultLabel.configure(text="  ACCESS DENIED  ")
                self.resultLabel.configure(bg="red")
                return True 
            else:
                lastSeenStr = self.lastSeenString(member.lastseen)
                self.resultLabel.configure(text="  " + member.name + ", " + member.forename + "  mitgliedsstatus " + member.membertype + "  lastseen: " + lastSeenStr + "  ")
    
                if "not yet" in lastSeenStr:
                    self.resultLabel.configure(bg="#00ff00")
                else:
                    self.resultLabel.configure(bg="yellow")
                return True 
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
        if messagebox.askquestion("Sure?", "Wirklich?") == 'no':
            return
        memberID = self.dataList.get(ACTIVE).split(":")[0]
        genCode = self.members.generateBadgecode()
        self.arduCon.writeTag(genCode)
        self.members.addBadgecode(memberID, genCode)
        self.updateList()


if __name__ == "__main__":
    Gui().start()



