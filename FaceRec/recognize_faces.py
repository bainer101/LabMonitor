import face_recognition
import argparse
import pickle
import cv2
import Menu

class recognize_faces:
    def __init__(self, encodings="encodings.pickle", detection_method="cnn"):
        self.encodings = encodings
        self.detection_method = detection_method

        self.data = None
        self.cap = None

    def main(self):
        while (True):
            self.cap = cv2.VideoCapture(0)
            self.date = pickle.loads(open(self.encodings, "rb").read())
            
            print ("[INFO] loading encodings...")
            _, image = self.cap.read()
            rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            print ("[INFO] recognizing faces...")
            boxes = face_recognition.face_locations(rgb, model=self.detection_method)
            encodings = face_recognition.face_encodings(rgb, boxes)

            names = []

            for encoding in encodings:
                matches = face_recognition.compare_faces(self.data["encodings"], encoding)
                name = "Unknown"

                if True in matches:
                    matchedIdxs = [i for (i, b) in enumerate (matches) if b]
                    counts = {}

                    for i in matchedIdxs:
                        name = self.data["names"][i]
                        counts[name] = counts.get(name, 0) + 1

                    name = max(counts, key=counts.get)
                names.append(name)

            for ((top, right, bottom, left), name) in zip(boxes, names):
                cv2.rectangle(image, (left, top), (right, bottom), (0, 255, 0), 2)
                y = top - 15 if top - 15 > 15 else top + 15
                
                cv2.putText(image, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
                            0.75, (0, 255, 0), 2)

            cv2.imshow("Image", image)
            if (cv2.waitKey(1) & 0xFF == ord('q')):
                break

        self.cap.release()
        cv2.destroyAllWindows()

        
        m = Menu.Menu()
        m.main()
