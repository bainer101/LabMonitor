import os
import cv2
from base_camera import BaseCamera

class Camera(BaseCamera):
    video_source = 0

    def __init__(self):
        # if specific camera defined as environment variable, open that, otherwise use system default
        if os.environ.get("OPENCV_CAMERA_SOURCE"):
            Camera.set_video_source(int(os.environ["OPENCV_CAMERA_SOURCE"]))
        super(Camera, self).__init__()

    @staticmethod
    def set_video_source(source):
        Camera.video_source = source

    @staticmethod
    def frames():
        camera = cv2.VideoCapture(Camera.video_source)
        if not camera.isOpened():
            raise RuntimeError("Could not start camera")

        while True:
            _, img = camera.read()

            yield cv2.imencode('.jpg', img)[1].tobytes()
