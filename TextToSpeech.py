import cv2
import time
import pyttsx3
import argparse
import pytesseract
import numpy as np

from PIL import Image
from threading import Thread

parser = argparse.ArgumentParser()
parser.add_argument("--no_camera", action="store_true", help="Process this program on local video")
args = parser.parse_args()

def detect(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    sobel = cv2.Sobel(gray, cv2.CV_8U, 1, 0, ksize = 3)
    ret, binary = cv2.threshold(sobel, 0, 255, cv2.THRESH_OTSU+cv2.THRESH_BINARY)
    element1 = cv2.getStructuringElement(cv2.MORPH_RECT, (30, 9))
    element2 = cv2.getStructuringElement(cv2.MORPH_RECT, (24, 6))

    dilation = cv2.dilate(binary, element2, iterations = 1)
    erosion = cv2.erode(dilation, element1, iterations = 1)
    dilation2 = cv2.dilate(erosion, element2, iterations = 3)
    
    region = []
    contours, hierarchy = cv2.findContours(dilation2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        area = cv2.contourArea(cnt) 
        if area < 1000:
            continue
        epsilon = 0.001 * cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, epsilon, True)

        x, y, w, h = cv2.boundingRect(cnt)
        '''
        rect = cv2.minAreaRect(cnt)
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        h = abs(box[0][1] - box[2][1])
        w = abs(box[0][0] - box[2][0])
        '''
        if h < w * 1.2:
            cv2.rectangle(img, (x,y), (x+w, y+h), (0, 255, 0), 2)
            #cv2.drawContours(img, [box], 0, (0, 255, 0), 2)
    return img


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
                frame = detect(self.frame)
                cv2.imshow('frame', frame)
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
        frame = TITS.get_frame()
        if frame is not None:
            image = Image.fromarray(frame)
            text = pytesseract.image_to_string(image, lang="chi_tra+eng")
            print(text)
            text_to_speech.say(text)
            text_to_speech.runAndWait()
            if TITS.is_stop():
                break
    
    