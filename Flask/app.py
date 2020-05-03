from importlib import import_module
import sys
from flask import *
import argparse
import cv2
import numpy as np
import os
import socket

parser = argparse.ArgumentParser(description="Run the flask web server")
parser.add_argument("hostname",
                    metavar="hostname",
                    type=str,
                    help="hostname for the web server")
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

@app.after_request
def add_header(response):
    response.cache_control.no_store = True
    return response

@app.route('/download_frame')
def download_frame():
    ident = Camera().send_ident()
    nparr = np.frombuffer(Camera().get_frame(), np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    name = str(ident) + ".jpg"
    file = "frames/" + name
    cv2.imwrite(file, img)

    resp = send_file(file)

    return resp

@app.route('/get_facial_encodings')
def get_facial_encodings():
    s = socket.socket()
    print ("Socket created")

    port = 50001

    s.bind(("", port))
    print ("Socket binded to port " + str(port))

    s.listen(5)
    print ("Socket is listening")

    c, addr = s.accept()
    print ("Got connection from " + str(addr))

    c.send(b'Thanks for connecting')

    c.close()

@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

if __name__ == '__main__':
    app.run(host=args.hostname, debug=True)
