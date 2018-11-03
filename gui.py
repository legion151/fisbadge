#!/usr/bin/python3

import data
import time
from tkinter import *
from threading import Thread


class Gui():
    def __init__(self):
        self.members = data.Members("data.csv")
        self.g = Tk()
        self.g.title = "Fis Badge"
        self.g.minsize(width=400,height=400)
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
            self.resultLabel.configure(text="Person: " + member.name + ", " + member.forename + "  lastseen:" + member.lastseen)
            self.resultLabel.configure(bg="green")


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
    time.sleep(2)
    global gui
    gui.showResult("")
    time.sleep(5)
    gui.showResult("USQvwllXLIIb3UCD")




if __name__ == "__main__":
    gui = Gui()

    worker = Thread(target=changeStuff)
    worker.start()

    gui.start()
