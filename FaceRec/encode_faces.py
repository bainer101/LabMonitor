from imutils import paths
import face_recognition
import argparse
import pickle
import cv2
import os
import Menu

class encode_faces:
    def __init__(self, dataset="dataset", encodings="encodings.pickle", detection_method="cnn"):
        self.dataset = dataset
        self.encodings = encodings
        self.detection_method = detection_method

        self.m = Menu.Menu()
        self.imagePaths = None
        self.knownEncodings = []
        self.knownNames = []

    def main(self):
        print("[INFO] quantifying faces...")
        self.imagePaths = list(paths.list_images(self.dataset))

        for (i, imagePath) in enumerate(self.imagePaths):
            print("[INFO] processing image {}/{}".format(i + 1, len(self.imagePaths)))
            name = imagePath.split(os.path.sep)[-2]
            print (name)

            image = cv2.imread(imagePath)
            rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            boxes = face_recognition.face_locations(rgb, model=self.detection_method)
            encodings = face_recognition.face_encodings(rgb, boxes)

            for encoding in encodings:
                self.knownEncodings.append(encoding)
                self.knownNames.append(name)

        self.storage()
        
        self.m.main()

    def storage(self):
        print ("[INFO] serializing encodings...")
        data = {"encodings": self.knownEncodings, "names": self.knownNames}
        f = open(self.encodings, "wb")
        f.write(pickle.dumps(data))
        f.close()

