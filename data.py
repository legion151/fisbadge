#!/usr/bin/python3

import datetime
import random, string, copy
import requests

class Members():
    def __init__(self, path):
        self.members = []
        self.path = path
        self.load()

    def proofMember(self,userkey):
        for member in self.members:
            if len(userkey)>0 and member.memberkey == userkey:
                memberCpy = copy.copy(member)
                member.updateLastSeen()
                self.persist()
                return memberCpy
        return None


    def addMemberKey(self, ID, key):
        for m in self.members:
            if m.ID==ID:
                m.memberkey = key
                m.updateLastSeen()
        self.persist()

    def getMembersByName(self, name, forename):
        filteredMembers = self.members
        filteredMembers = filter(lambda e: len(e.memberkey)==0, filteredMembers)
        if len(name)>0:
            filteredMembers = filter(lambda e: e.name.startswith(name), filteredMembers)
        if len(forename)>0:
            filteredMembers = filter(lambda e: e.forename.startswith(forename), filteredMembers)
        return filteredMembers 


    def generateMemberKey(self):
        return "".join(random.choice(string.ascii_letters+string.digits) for i in range(16))

    def persist(self):
        f = open(self.path, "w")
        f.write("id,name,forename,membertype,birthday,memberkey\n")
        f.writelines([member.getCSVLine()+"\n" for member in self.members])
        f.close()

    def load(self):
        self.members = []
        with open(self.path) as f:
            dataArray = f.readlines()
            for dataLine in dataArray[1:]:
                dataLine=dataLine.strip()
                member = Member(dataLine.split(","))
                self.members.append(member)

    def pullData(self, usr, pwd):
        url = "https://www.fis-ev.de/intern/db/getFisBadgeFile.php"
        data = requests.get(url, auth=(usr, pwd)).content.decode()

        if 'id,name,forename' in data:
            open(self.path, "w").write(data)
            self.load()
            return True

        else:
            print(data)
            return False




class Member():
    def __init__(self, memberentry):
        self.ID = memberentry[0]
        self.name = memberentry[1]
        self.forename = memberentry[2]
        self.membertype = memberentry[3]
        self.birthday = memberentry[4]
        self.lastseen = "not yet" 
        self.memberkey = memberentry[5]

    def updateLastSeen(self):
        self.lastseen = str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    def __str__(self):
        return self.getCSVLine()


    def getCSVLine(self):
        csv = ""
        csv += str(self.ID) + ","
        csv += str(self.name) + ","
        csv += str(self.forename) + ","
        csv += str(self.membertype) + ","
        csv += str(self.birthday) + ","
        csv += str(self.memberkey)
        return csv

