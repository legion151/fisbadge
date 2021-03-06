#!/usr/bin/python3

import datetime
import random, string, copy
import requests

def dbg(s, err=""):
    if(len(err)>0):
        print(f"dateModul: {s} err: {err}")
    else:
        print(f"dateModul: {s}")

class Members():
    def __init__(self, path):
        self.members = []
        self.path = path
        self.load()

    def proofMember(self,userkey):
        dbg(f"proofing: {userkey}")
        for member in self.members:
            dbg(f"cur mem: {member.badgecode}")
            if len(userkey)>0 and member.badgecode.encode("utf-8") == userkey:
                memberCpy = copy.copy(member)
                member.updateLastSeen()
                self.persist()
                return memberCpy
        dbg(f"returning none")
        return None

    def addBadgecode(self, ID, badgecode):
        for m in self.members:
            if m.ID==ID:
                m.badgecode = badgecode
                m.updateLastSeen()
        self.persist()

    def getMembersByName(self, name, forename, showRegistered=False):
        filteredMembers = self.members
        if not showRegistered:
            filteredMembers = filter(lambda e: len(e.badgecode)==0, filteredMembers)
        if len(name)>0:
            filteredMembers = filter(lambda e: name.lower() in e.name.lower(), filteredMembers)
        if len(forename)>0:
            filteredMembers = filter(lambda e: forename.lower() in e.forename.lower(), filteredMembers)
        return filteredMembers 


    def generateBadgecode(self):
        return "".join(random.choice(string.ascii_letters+string.digits) for i in range(16))

    def persist(self):
        with open(self.path, "w") as f:
            f.write("id,name,forename,membertype,birthday,badgecode\n")
            f.writelines([member.getCSVLine()+"\n" for member in self.members])

    def load(self):
        self.members = []
        try:
            with open(self.path) as f:
                dataArray = f.readlines()
                for dataLine in dataArray[1:]:
                    dataLine=dataLine.strip()
                    member = Member(dataLine.split(","))
                    self.members.append(member)
        except:
            pass

    def pullData(self, usr, pwd):
        try:
            url = "https://www.fis-ev.de/intern/db/getFisBadgeFile.php"
            data = requests.get(url, auth=(usr, pwd), timeout=5).content.decode()

            if 'id,name,forename' in data:
                open(self.path, "w").write(data)
                self.load()
                return True

            else:
                return False
        except:
            return False

    def pushData(self, usr, pwd):
        try:
            url = "https://www.fis-ev.de/intern/db/setFisBadgeData.php"
            postdata = ""
            for member in self.members:
                if member.badgecode:
                    postdata += member.ID +","+ member.badgecode + ";"
    
            payload = {"data":postdata}
            r = requests.post(url, auth=(usr, pwd), data=payload, timeout=5).content.decode()
    
            return 'success' in r
        except:
            return False



class Member():
    def __init__(self, memberentry):
        self.ID = memberentry[0]
        self.name = memberentry[1]
        self.forename = memberentry[2]
        self.membertype = memberentry[3]
        self.birthday = memberentry[4]
        self.lastseen = "not yet" 
        self.badgecode = memberentry[5]

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
        csv += str(self.badgecode)
        return csv

