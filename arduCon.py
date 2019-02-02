import serial



class RFID_Conn:
    def __init__(self):
        self.connect()

    def connect(self):
        self.ser = serial.Serial(timeout=0, baudrate=9600)
        self.ser.port = '/dev/ttyUSB0'

        self.ser.open()


    def send(self, data):
        self.ser.write(data.encode('utf-8'))

    def p(self):
        print(self.ser.readall())



if __name__=="__main__":
    con = RFID_Conn()

    con.p()


