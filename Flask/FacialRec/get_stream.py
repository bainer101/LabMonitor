import cv2
import time

while True:
    cap = cv2.VideoCapture("http://127.0.0.1:5000/video_feed")
    if (cap.isOpened()):
        ret, img = cap.read()
        cv2.imshow("win", img)

        k = cv2.waitKey(10) & 0XFF
        if (k == 27):
            break
