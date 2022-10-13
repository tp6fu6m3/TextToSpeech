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
        self.thread = Thread(target=self.update, args=())
        self.thread.daemon = True
        self.thread.start()
        
        self.engine = pyttsx3.init()

    def update(self):
        while True:
            if self.capture.isOpened():
                (self.status, self.frame) = self.capture.read()
            time.sleep(self.FPS)

    def show_frame(self):
        cv2.imshow('frame', self.frame)
        cv2.waitKey(self.FPS_MS)
        
    def frame2audio(self):
        img = Image.fromarray(self.frame)
        text = pytesseract.image_to_string(img, lang="chi_tra+eng")
        print(text)
        self.engine.say(text)
        self.engine.runAndWait()


if __name__ == '__main__':
    capture = ThreadedCamera()
    while True:
        try:
            capture.show_frame()
            capture.frame2audio()
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                break
        except AttributeError:
            pass

