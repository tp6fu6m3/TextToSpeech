import cv2
import time
import pyttsx3
import argparse
import pytesseract

from PIL import Image
from threading import Thread

parser = argparse.ArgumentParser()
parser.add_argument("--no_camera", action="store_true", help="Process this program on local video")
args = parser.parse_args()

class ThreadedCamera(object):
    def __init__(self):
        self.capture = cv2.VideoCapture(0)
        self.capture.set(cv2.CAP_PROP_BUFFERSIZE, 2)

        self.FPS = 1/30
        self.FPS_MS = int(self.FPS * 1000)

        # Start frame retrieval thread
        self.tupdate = Thread(target=self.update)
        self.tupdate.daemon = True
        self.tshow_frame = Thread(target=self.show_frame)
        self.tshow_frame.daemon = True
        #self.tframe2audio = Thread(target=self.frame2audio)
        #self.tframe2audio.daemon = True
        
        self.stop = False
        #self.engine = pyttsx3.init()
    
    def forward(self):
        self.tupdate.start()
        time.sleep(1)
        self.tshow_frame.start()
        time.sleep(1)
        #self.tframe2audio.start()
        #time.sleep(1)
        
    
    def update(self):
        while True:
            if self.capture.isOpened():
                (self.status, self.frame) = self.capture.read()
            time.sleep(self.FPS)

    def show_frame(self):
        while True:
            try:
                cv2.imshow('frame', self.frame)
                if cv2.waitKey(self.FPS_MS) & 0xFF == ord('q'):
                    cv2.destroyAllWindows()
                    self.stop = True
            except:
                print("An show_frame exception occurred")

    def frame2audio(self):
        while True:
            img = Image.fromarray(self.frame)
            text = pytesseract.image_to_string(img, lang="chi_tra+eng")
            print(text)
            self.engine.say(text)
            self.engine.runAndWait()



if __name__ == '__main__':
    engine = pyttsx3.init()
    capture = ThreadedCamera()
    capture.forward()
    while True:
        img = Image.fromarray(capture.frame)
        text = pytesseract.image_to_string(img, lang="chi_tra+eng")
        print(text)
        engine.say(text)
        engine.runAndWait()
        if capture.stop:
            break
    
    