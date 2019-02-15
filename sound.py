import time
import playsound

class Sound:
    def __init__(self):
        self.goodFile = "./sound/good.wav"
        self.badFile = "./sound/bad.wav"


    def play(self, good):
        try:
            if(good):
                playsound.playsound(self.goodFile)
            else:
                playsound.playsound(self.badFile)
        except:
            print("error in sound")


if __name__=="__main__":
    s=Sound()
    s.play(False)
