import cv2
import time
import pyttsx3
import argparse
import pytesseract

from PIL import Image
from threading import Thread, Lock

parser = argparse.ArgumentParser()
parser.add_argument("--no_camera", action="store_true", help="Process this program on local video")
args = parser.parse_args()

class TextImageToSpeech():
    def __init__(self):
        #self.capture = cv2.VideoCapture(0)
        self.capture = cv2.VideoCapture('sample_video.mp4') if (args.no_camera) else cv2.VideoCapture(0)
        self.capture.set(cv2.CAP_PROP_BUFFERSIZE, 2)
        #self.capture.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
        #self.capture.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'P', '4', 'V'))

        self.FPS = 1/30
        self.FPS_MS = int(self.FPS * 1000)

        self.thread_read_frame = Thread(target=self.read_frame, daemon=True)
        self.thread_show_frame = Thread(target=self.show_frame, daemon=True)
        self.stop = False
        
    
    def read_frame(self):
        while True:
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
                print("An exception occurred")
    
    def camera_is_open(self):
        return args.no_camera or self.capture.isOpened()
        
    def run_thread(self):
        self.thread_read_frame.start()
        time.sleep(1)
        self.thread_show_frame.start()
        time.sleep(1)
    
    def get_frame(self):
        return self.frame
        
    def is_stop(self):
        return self.stop
        


if __name__ == '__main__':
    text_to_speech = pyttsx3.init()
    TITS = TextImageToSpeech()
    assert TITS.camera_is_open()
    TITS.run_thread()
    while True:
        image = Image.fromarray(TITS.get_frame())
        text = pytesseract.image_to_string(image, lang="chi_tra+eng")
        print(text)
        text_to_speech.say(text)
        text_to_speech.runAndWait()
        if TITS.is_stop():
            break
    
    