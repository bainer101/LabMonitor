import time
import threading
import os

try:
    from greenlet import getcurrent as get_ident
except ImportError:
    try:
        from thread import get_ident
    except ImportError:
        from _thread import get_ident

class CameraEvent(object):
    # Creates an event when new frame is available

    def __init__(self):
        self.events = {}

    def wait(self):
        ident = get_ident()
        if ident not in self.events:
            # This is a new client
            # Add the threading.Event() and timestamp to events dict
            self.events[ident] = [threading.Event(), time.time()]
        return self.events[ident][0].wait()

    def set(self):
        now = time.time()
        remove = None
        for ident, event in self.events.items():
            if not event[0].isSet():
                event[0].set()
                event[1] = now
            else:
                if now - event[1] > 5:
                    remove = ident
        if remove:
            del self.events[remove]

    def clear(self):
        self.events[get_ident()][0].clear()

class BaseCamera(object):
    thread = None
    frame = None
    last_access = 0
    event = CameraEvent()

    def __init__(self):
        if BaseCamera.thread is None:
            BaseCamera.last_access = time.time()

            BaseCamera.thread = threading.Thread(target=self._thread)
            BaseCamera.thread.start()

            while self.get_frame() is None:
                time.sleep(0)

    def get_frame(self):
        BaseCamera.last_access = time.time()
        BaseCamera.event.wait()
        BaseCamera.event.clear()

        return BaseCamera.frame

    def send_ident(self):
        return get_ident()

    @staticmethod
    def clean_frames():
        dir = "frames"
        filesToRemove = [os.path.join(dir, f) for f in os.listdir(dir)]
        for f in filesToRemove:
            os.remove(f)

    @staticmethod
    def frames():
        raise RuntimeError("Must be implemented by subclasses")

    @classmethod
    def _thread(cls):
        print ("Starting camera thread")
        frames_iterator = cls.frames()

        for frame in frames_iterator:
            BaseCamera.frame = frame
            BaseCamera.event.set()
            time.sleep(0)

            # stop thread if no clients requesting frames
            if time.time() - BaseCamera.last_access > 10:
                frames_iterator.close()
                BaseCamera.clean_frames()
                print ("Stopping camera thread due to inactivity")
                break
        BaseCamera.thread = None
