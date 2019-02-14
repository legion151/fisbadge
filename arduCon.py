import serial, random, glob, time, sys

def dbg(s, err=""):
    if(err):
        print(f"arduCon: {s} err: {err}")
    else:
        print(f"arduCon: {s}")


class Ardu:
    def __init__(self):
        self.connected = False

    def connect(self):
        if(not self.connected):
            dbg("searching port")
            self.ser = serial.Serial(timeout=1, baudrate=9600)# , xonxoff=0, rtscts=0, dsrdtr=0)
            ports = glob.glob("/dev/ttyUSB*")
            for p in ports:
                dbg("try port: " + str(p))
                self.ser.port = p
                try:
                    self.ser.open()
                    time.sleep(5)
                    self.ser.flush()
                    if(self.pingpong()):
                        return True
                except Exception as e:
                    dbg("exception during open" , str(e))
                    return False
        else:
            return self.pingpong()

    def pingpong(self): 
        try:
            dbg("write synword")
            self.ser.flush()
            sentBytes = 0
            sentBytes += self.ser.write(b'FIS')
            dbg(sentBytes)
            self.ser.flush()
            result = self.ser.read(5)
            self.ser.flush()
            dbg("got: " + str(result))
            if result.find(b'BADGE') >= 0:
                self.connected = True
                return True
            else:
                self.connected = False
                return False
        except:
            dbg("exception occured", err=sys.exc_info()[1])
            self.connected = False
            return False

    def send(self, data):
        try:
            self.ser.write(data.encode('utf-8'))
        except:
            self.connected = False
    def read(self):
        try:
            return self.ser.read(16)
        except:
            self.connected = False
        

    def getScanResult(self):
        results = ["pd36Qwyj7s7NQvZ4", "pd36Qwyj7s7NQvZt", "ILZRLOe4x7nu2MRA", "JHEQOvaOGj55s71W"]
        if random.randint(1,10) == 1:
            return random.choice(results)
        else:
            return ""
    def writeTag(self, s):
        dbg("i should write tag with: " + str(s))
        


if __name__=="__main__":
    con = Ardu()
    while True:
        con.connect()
        time.sleep(.200)




