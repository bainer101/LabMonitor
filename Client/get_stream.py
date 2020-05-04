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
                    help="IP address of Flask server")
parser.add_argument("port",
                    metavar="port",
                    type=str,
                    help="port of flask server")
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
    print ("3 seconds until images are taken")
    time.sleep(3)
    knownEncodings = []

    for i in range(1, args.frames+1):
        frame = url_to_image("http://" + args.ip + ":" + args.port + "/download_frame")
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

    print ("Completed encodings")

    return json.dumps(data)

hasConnected = False
port = 12345

while True:
    while not hasConnected:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((args.ip, port))
            hasConnected = True
        except Exception as e:
            s.close()

    datachunk = s.recv(1024)

    while not datachunk:
        continue

    if datachunk.decode("utf-8") == "facial_encodings":
        hasConnected = False
        s.close()

        s = socket.socket()
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        print ("Socket created")

        s.bind(("", 54321))
        print ("Socket binded to port " + str(port))

        s.listen(5)
        print ("Socket is listening")

        c, addr = s.accept()

        print ("Got connection from " + str(addr))

        encodings = run_on_listen()
        c.sendall(bytes(encodings,encoding="utf-8"))
        c.close()

        print("\nWaiting on request")

s.close()
