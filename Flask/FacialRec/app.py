#!/usr/bin/env python
from importlib import import_module
import sys
from flask import Flask, render_template, Response
import argparse

parser = argparse.ArgumentParser(description="Run the flask web server")
parser.add_argument("--pi", action="store_true", help="Using the Pi Cam")

args=parser.parse_args()

if args.pi:
    Camera = import_module("camera_pi").Camera
else:
    Camera = import_module("camera_opencv").Camera

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(Camera()),
    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=True)
