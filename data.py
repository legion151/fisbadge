
import datetime
from dateutil.parser import parse
import random
class Members():
    self.fileObject
    self.dataArray
    self.dataDictionary = {}

    def __init__(self):
        #read file and store to internal mem
        self.loadDataFromFile(pathAndFileName)


    def proofMember(self,userkey):
        #should return name, forename, lastseen
        # as tuple
        #empty tuple if user is not in list
        if(self.dataDictionary.has_key(userkey))
        return dataDictionary[userkey]
        else
        return{}

    def addMember(self, id, name, forname):
        this.generateUserKey(id,name,forname)
        this.persist()
        #add to internal
        #persist


    def generateUserKey(self,id,name, forename):
        mMember = Member.__init__(id,name,forname)
        sKey = mMember.getKey()
        dataDictionary[key] = mMember.addMemberToDictionary()
        #Generate random Key, add Data given from GUI, save into file...?... Profit


    def persist(self):
        #save internal storage
        #should be invoked by addmember
        self.fileObject.open()
            with iIndex in self.dataDictionary
            self.fileObject.write(self.dataDictionary.values())

        self.fileObject.open()

    def loadDataFromFile(self,pathAndFileName):
        #Load data from File the file should be in the same directory
        with open(pathAndFileName,"r+") as fileObject
        dataArray = fileObject.readlines()
         for iIndex in dataArray
            dataLine = dataArray[iIndex]
            key = dataLine[5]
            value = dataLine
            dataDictionary[key] = value


class Member():
    def __init__(self, id, sMemberName,sMemberFirstName):
        self.id = id
        self.name = sMemberName
        self.firstname = sMemberFirstName
        self.datetime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.key =  random.randint(1,4294967295)

    def addMemberToDictionary(self):
        return [self.id,self.name,self.firstname,self.datetime,self.key]

    def getKey(self):
        return self.key
    def getName(self):
        return self.name
    def getForName(self)
        return self.firstname
    def getlastSeen(self)
        return self.datetime
    def getId(self)
        return self.id





if __name__ == "__main__": 
    print("testprogram")
    do stuff with your class
