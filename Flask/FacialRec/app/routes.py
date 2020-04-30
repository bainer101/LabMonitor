from app import app
from flask import Flask, render_template, Response
import cv2

@app.route('/')
@app.route('/index.html')
def index():
    return render_template("index.html")

def gen(camera):
    _, frame = camera.read()
    yield cv2.imencode('.jpg', frame)[1].tobytes()

@app.route('/video_feed')
def video_feed():
    return Response(gen(cv2.VideoCapture(0)),
                mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='127.0.0.1:5000', debug=True)
