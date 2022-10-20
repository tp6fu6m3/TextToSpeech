import cv2
import json

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
assert cap.isOpened()
with open("resolutionList.json", 'r') as f:
    resolutionList = json.load(f)
print('開始測試攝影機支援的解析度')
max_width = 0
max_height = 0
for p in resolutionList:
    width = p['width']
    height = p['height']
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    rw = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    rh = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    if rw == width and rh == height:
        print('{} x {}: OK'.format(width, height))
        max_width, max_height = width, height
print('{} x {} is the best'.format(max_width, max_height))
cap.release()









