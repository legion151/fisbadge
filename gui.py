#!/usr/bin/python3

import data
import time
import datetime
from tkinter import *
from threading import Thread


class Gui():
    def __init__(self):
        self.members = data.Members("data.csv")
        self.g = Tk()
        self.g.title = "Fis Badge"
        self.g.minsize(width=600,height=600)
        self.title = Label(self.g, pady=20, padx=20, font=("Arial", 24), text="FiS - RFID Badge Controller")
        self.title.grid(row=0, columnspan=2)
        self.resultLabel = Label(self.g, font=("Arial", 18), text="Person: ")
        self.resultLabel.grid(row=1, columnspan=2)

        self.createAreaTitle= Label(self.g, pady=50, font=("Arial", 16), text="Write tag: ")
        self.createAreaTitle.grid(row=2, columnspan=2)

        self.createAreaTitle= Label(self.g, pady=10, font=("Arial", 16), text="Filter Name: ")
        self.createAreaTitle.grid(row=3, column=0, sticky=E)
        self.nameInput = Entry(self.g,  width=20)
        self.nameInput.grid(row=3, column=1, sticky=W)
        self.nameInput.bind("<Key>", self.updateList)

        self.createAreaTitle= Label(self.g, pady=10, font=("Arial", 16), text="Filter Vorname: ")
        self.createAreaTitle.grid(row=4, column=0, sticky=E)
        self.forenameInput = Entry(self.g, width=20)
        self.forenameInput.bind("<Key>", self.updateList)
        self.forenameInput.grid(row=4, column=1, sticky=W)

        self.dataList = Listbox(self.g, width=80)
        self.dataList.bind("<Button-1>", lambda : self.addBtn.configure(state="normal"))

        self.updateList(None)
        self.dataList.grid(row=5, columnspan=2, padx=20)

        self.addBtn = Button(self.g, text="Tag schreiben",  command=lambda : self.addBtnAck.configure(state="normal"), state="disabled")
        self.addBtn.grid(row=6, column=0, sticky=E)
        self.addBtnAck = Button(self.g, text="Bestätigen",  command=self.addBtnAction, state="disabled")
        self.addBtnAck.grid(row=6, column=1, sticky=W)

    def start(self):
        self.g.mainloop()

    def showResult(self, memberKey):
        member = self.members.proofMember(memberKey)
        if not member:
            self.resultLabel.configure(text="Person: not found")
            self.resultLabel.configure(bg="red")
        else:
            lastSeenStr = self.lastSeenString(member.lastseen)
            self.resultLabel.configure(text="Person: " + member.name + ", " + member.forename + "  lastseen: " + lastSeenStr + " ago")

            if "days" in lastSeenStr:
                self.resultLabel.configure(bg="#00ff00")
            else:
                self.resultLabel.configure(bg="yellow")

    def lastSeenString(self, datestring):
        d_last = datetime.datetime.strptime(datestring.strip(), "%Y-%m-%d %H:%M:%S")
        d_now = datetime.datetime.now()
        dif = d_now-d_last

        if(dif.days>0):
            return str(dif.days) + " days"
        secs = dif.seconds
        if(secs // 3600)>0:
            return str(secs//3600) + " hours"
        if(secs //60)>0:
            return str(secs//60) + " minutes"
        return str(secs) + " secs"

    def addBtnAction(self):
        memberID = self.dataList.get(ACTIVE).split(":")[0]
        self.members.addMemberKey(memberID, self.members.generateMemberKey())
        self.updateList(None)
        self.addBtnAck.configure(state="disabled")


    def updateList(self, eve):
        self.dataList.delete(0,END)
        name = self.nameInput.get()
        print(name)
        forename = self.forenameInput.get()
        print(forename)
        filteredMembers = self.members.getMembersByName(name, forename) 

        for member in filteredMembers:
            self.dataList.insert(END, member.ID + ": " + member.name + ", " + member.forename + "   geboren " + member.birthday)



def changeStuff():
    time.sleep(1)
    global gui
    gui.showResult("")
    time.sleep(1)
    gui.showResult("USQvwllXLIIb3UCD")
    time.sleep(1)
    gui.showResult("sAiTrBk679pnrwK1")
    time.sleep(3)
    gui.g.quit()



if __name__ == "__main__":
    gui = Gui()

    worker = Thread(target=changeStuff)
    worker.start()

    gui.start()
