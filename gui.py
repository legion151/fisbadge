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
        self.title = Label(self.g, pady=20, padx=20, font=("Arial", 24), text="FiS - RFID Badge Controller", anchor=CENTER, justify=CENTER)
        self.title.pack()
        self.resultLabel = Label(self.g, font=("Arial", 18), text="Person: ", anchor=CENTER)
        self.resultLabel.pack()

        self.createAreaTitle= Label(self.g, pady=30, font=("Arial", 16), text="Create entry: ", anchor=W)
        self.createAreaTitle.pack()

        self.createAreaTitle= Label(self.g, pady=10, font=("Arial", 16), text="Name: ", anchor=W)
        self.createAreaTitle.pack()
        self.nameInput = Entry(self.g,  width=20)
        self.nameInput.pack()
        self.nameInput.bind("<Key>", self.updateList)

        self.createAreaTitle= Label(self.g, pady=10, font=("Arial", 16), text="Vorname: ", anchor=W)
        self.createAreaTitle.pack()
        self.forenameInput = Entry(self.g, width=20)
        self.forenameInput.bind("<Key>", self.updateList)
        self.forenameInput.pack()

        self.dataList = Listbox(self.g, width=60)

        self.updateList(None)
        self.dataList.pack()

        self.addBtn = Button(self.g, text="Tag registrieren",  command=self.addBtnAction)
        self.addBtn.pack()

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



if __name__ == "__main__":
    gui = Gui()

    worker = Thread(target=changeStuff)
    worker.start()

    gui.start()
