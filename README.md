# Lab Monitor

This project allows users to retrieve data about the current state of their lab.

### Prerequisites
You will need to have a device with a webcam attached, preferably a Raspberry Pi with Pi Cam due to the size, and a PC with designated GPU which are on the same network.

#### Device with webcam
```
OpenCV - pip install opencv-python
Numpy - pip install numpy
A C++ compiler
dlib - pip install dlib
face_recognition - pip install face_recognition
pi_camera - only required if using Pi Cam
```

#### PC with dedicated GPU
```
OpenCV - pip install opencv-python
Numpy - pip install numpy
A C++ compiler
dlib - pip install dlib
face_recognition - pip install face_recognition
```

### Installing
Clone the GitHub repository and put the Flask folder on the device with webcam, and the Client folder on the PC with dedicated GPU.

#### PC with dedicated GPU
Run the script `get_stream` whilst supplying the following parameters:
* ip - the IP address of the Flask server
* port - the port that the Flask server is run on
* frames - the number of frames to take for facial encodings
##### Example
```
python3 get_stream.py 192.168.0.46 5000 5
```

#### Device with webcam
Run the script `app` whilst supplying the following parameters:
* hostname - the hostname to run the Flask server on
* ip - the IP address of the PC
* --pi - optional parameter set if you're using a Pi Cam
##### Example
```
python3 app.py 192.168.0.46 192.168.0.41
```
