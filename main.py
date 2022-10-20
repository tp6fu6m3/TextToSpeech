import cv2
import time
import pyttsx3
import argparse
import pytesseract
import numpy as np

from PIL import Image
from threading import Thread

LOCAL_URL = '192.168.31.72:8081'

parser = argparse.ArgumentParser()
parser.add_argument('--camera', action='store_true', help='Process this program on camera')
parser.add_argument('--no_camera', action='store_true', help='Process this program on local video')
args = parser.parse_args()

def detect(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #gray = cv2.fastNlMeansDenoising(gray, None, 10, 7, 21)
    #邊緣檢測
    sobel = cv2.Sobel(gray, cv2.CV_8U, 1, 0, ksize = 3)
    #二值化自動計算最佳閥值
    _, binary = cv2.threshold(sobel, 0, 255, cv2.THRESH_OTSU+cv2.THRESH_BINARY)
    #_, binary1 = cv2.threshold(sobel, 180, 255, cv2.THRESH_OTSU+cv2.THRESH_BINARY_INV)
    element1 = cv2.getStructuringElement(cv2.MORPH_RECT, (30, 9))
    element2 = cv2.getStructuringElement(cv2.MORPH_RECT, (24, 6))
    
    #影像膨脹
    dilation = cv2.dilate(binary, element2, iterations = 1)
    #影像侵蝕去噪
    erosion = cv2.erode(dilation, element1, iterations = 1)
    dilation2 = cv2.dilate(erosion, element2, iterations = 3)
    
    blur_img = cv2.GaussianBlur(img, (0, 0), 5)
    usm = cv2.addWeighted(img, 1.5, blur_img, -0.5, 0)
    bounding_images = []
    bounding_box = np.zeros(img.shape, np.uint8)
    contours, hierarchy = cv2.findContours(dilation2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area < (img.shape[0] * img.shape[1] / 120):
            continue
        
        x, y, w, h = cv2.boundingRect(cnt)
        if h > w * 2.0:
            continue
        cv2.rectangle(bounding_box, (x,y), (x+w, y+h), (0, 255, 0), 2)
        bounding_images.append(usm[y:y+h, x:x+w])
    return bounding_images, bounding_box


class TextImageToSpeech():
    def __init__(self):
        if (args.no_camera):
            self.capture = cv2.VideoCapture('sample_video.mp4')
        elif (args.camera):
            self.capture = cv2.VideoCapture(0)
        else:
            self.capture = cv2.VideoCapture('http://admin:admin@{}'.format(LOCAL_URL))
        
        self.capture.set(cv2.CAP_PROP_BUFFERSIZE, 2)
        #self.capture.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
        #self.capture.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'P', '4', 'V'))
        
        self.FPS = 1/30
        self.FPS_MS = int(self.FPS * 1000)
        
        self.frame = None
        self.stop = False
        self.bounding_images = []
        self.bounding_box = None
        
        self.thread_show_frame = Thread(target=self.show_frame, daemon=True)
        self.thread_detect_text = Thread(target=self.detect_text, daemon=True)
    
    def show_frame(self):
        while True:
            try:
                (status, self.frame) = self.capture.read()
                #time.sleep(self.FPS)
                
                if self.bounding_box is not None:
                    frame = cv2.add(self.frame, self.bounding_box)
                else:
                    frame = self.frame
                cv2.imshow('frame', frame)
                cv2.waitKey(30)
                if cv2.waitKey(self.FPS_MS) & 0xFF == ord('q'):
                    cv2.destroyAllWindows()
                    self.stop = True
            except:
                print('An exception occurred')
    
    def detect_text(self):
        while True:
            if self.frame is not None:
                try:
                    self.bounding_images, self.bounding_box = detect(self.frame)
                except:
                    print('An exception occurred')
    
    def camera_is_open(self):
        return args.no_camera or self.capture.isOpened()
        
    def run_thread(self):
        self.thread_show_frame.start()
        time.sleep(1)
        self.thread_detect_text.start()
        time.sleep(1)
    
    def get_bounding_images(self):
        return self.bounding_images
        
    def is_stop(self):
        return self.stop

def main():
    text_to_speech = pyttsx3.init()
    TITS = TextImageToSpeech()
    assert TITS.camera_is_open()
    TITS.run_thread()
    while True:
        bounding_images = TITS.get_bounding_images()
        for image in bounding_images:
            image = Image.fromarray(image)
            text = pytesseract.image_to_string(image, lang='chi_tra+eng')
            print(text)
            text_to_speech.say(text)
            text_to_speech.runAndWait()
            if TITS.is_stop():
                return

if __name__ == '__main__':
    main()
    

