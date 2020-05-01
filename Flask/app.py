#!/usr/bin/env python
from importlib import import_module
import sys
from flask import Flask, render_template, Response, send_file
import argparse
import cv2
import numpy as np

parser = argparse.ArgumentParser(description="Run the flask web server")
parser.add_argument("--pi", action="store_true", help="Using the Pi Cam")

args=parser.parse_args()

if args.pi:
    Camera = import_module("camera_pi").Camera
else:
    Camera = import_module("camera_opencv").Camera

app = Flask(__name__)
frame = None

@app.route('/')
def index():
    return render_template("index.html")

def gen():
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    global camera
    camera = Camera()
    return Response(gen(),
    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/download_frame')
def download_frame():
    ident = camera.get_ident()
    nparr = np.fromstring(camera.get_frame(), np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    cv2.imwrite("C:/Users/Alex/github/Flask/frames/" + str(ident) + ".jpg", img)
    return "HELLO"
    #return send_file("C:/Users/Alex/github/Flask/frames/" + str(ident) + ".jpg",
    #as_attachment=True)

if __name__ == '__main__':
    app.run(host='192.168.0.41', debug=True)
