import time
import playsound
from threading import Thread


class Sound:
    def __init__(self):
        self.goodFile = "./sound/good.wav"
        self.badFile = "./sound/bad.wav"


    def good(self):
        Thread(target=self.playGood).start()

    def bad(self):
        Thread(target=self.playBad).start()

    def playGood(self):
        self.play(True)
    def playBad(self):
        self.play(False)

    def play(self, good):
        try:
            if(good):
                playsound.playsound(self.goodFile)
            else:
                playsound.playsound(self.badFile)
        except Exception as e:
            print("error in sound" + str(e))



if __name__=="__main__":
    s=Sound()
    s.play(False)
