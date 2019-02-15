import serial, random, glob, time, sys

def dbg(s, err=""):
    if(err):
        print(f"arduCon: {s} err: {err}")
    else:
        print(f"arduCon: {s}")


class Ardu:
    def __init__(self):
        self.connected = False
        self.pingPongCount = 0

    def connect(self):
        if(not self.connected):
            try:
                self.ser.close()
            except:
                pass
            dbg("searching port")
            self.ser = serial.Serial(timeout=1, baudrate=9600)# , xonxoff=0, rtscts=0, dsrdtr=0)
            ports = glob.glob("/dev/ttyUSB*")
            for p in ports:
                dbg("try port: " + str(p))
                self.ser.port = p
                try:
                    self.ser.open()
                    time.sleep(2)
                    self.ser.flush()
                    if(self.pingpong()):
                        return True
                except Exception as e:
                    dbg("exception during open" , str(e))
                    return False
        else:
            return self.pingpong()

    def pingpong(self): 
        self.pingPongCount +=1
        if(self.pingPongCount%10 == 0):
            self.connected = False
            return False

        try:
            dbg("syn")
            self.ser.flush()
            self.ser.write(b'FIS')
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



    def readTag(self):
        try:
            return self.ser.read(16)
        except:
            self.connected = False
        
    def writeTag(self, s):
        dbg("i should write tag with: " + str(s))
        self.send(s)
        


if __name__=="__main__":
    con = Ardu()
    while True:
        con.connect()
        time.sleep(.200)




