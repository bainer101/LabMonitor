import cv2
from imutils import paths
import face_recognition
import os
import time
import json
import urllib
import numpy as np
import argparse
import socket

parser = argparse.ArgumentParser(description="Return facial encodings to site")
parser.add_argument("ip",
                    metavar="ip",
                    type=str,
                    help="IP address of Flask server (including port)")
parser.add_argument("frames",
                    metavar="frames",
                    type=int,
                    help="number of frames to be taken")
args=parser.parse_args()

def url_to_image(url):
    resp = urllib.request.urlopen(url)
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)

    return image

def run_on_listen():
    print ("3 seconds till images are taken")
    time.sleep(3)
    knownEncodings = []

    for i in range(args.frames):
        frame = url_to_image("http://" + args.ip + "/download_frame")
        print("Reading image:" + str(i) + "/" + str(args.frames))
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        boxes = face_recognition.face_locations(rgb,
        model="hog")

        encodings = face_recognition.face_encodings(rgb, boxes)

        print("Encoding image:" + str(i) + "\n")

        for encoding in encodings:
            knownEncodings.append(encoding)

    for i, knownEncoding in enumerate(knownEncodings):
        knownEncodings[i] = knownEncoding.tolist()

    data = {"encodings": knownEncodings}
    with open('encodings.json', 'w') as fp:
        json.dump(data, fp)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
print (args.ip)
s.bind(("192.168.0.46", 50001))
s.listen(1)
conn,address=s.accept()

while True:
    datachunk = conn.recv(1024)
    if not datachunk:
        break
    print (datachunk)

conn.close()
