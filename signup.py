import encode_faces
import numpy as np
import cv2
import os
import time

class signup:
    def __init__(self):
        self.cap = None
        self.counter = 0
        self.capturing = False
        self.name = ""
        self.frame = None

    def main(self):
        self.cap = cv2.VideoCapture(0)
        
        while (self.counter < 100):
            _, self.frame = self.cap.read()
            cv2.imshow ("frame", self.frame)

            if (self.capturing):
                cv2.imwrite("dataset/" + self.name + "/" + str(self.counter)
                    + ".jpg", self.frame)
                self.counter += 1
                time.sleep(0.2)

            if (cv2.waitKey(1) & 0xFF == ord(' ')):
                self.start()
        
        self.cap.release()
        cv2.destroyAllWindows()
        ef = encode_faces.encode_faces()
        ef.main()

    def start(self):
        self.name = input("Please enter your full name: ")
        self.name = self.name.replace(" ", "_")

        if (not os.path.exists("dataset/" + self.name)):
            os.mkdir("dataset/" + self.name)

        for x in range(3, 0, -1):
            print (x)
            time.sleep(1)

        print ("Pose")
        self.capturing = True
