from VideoCamera import VideoCamera
from FaceDetector import FaceDetector
from ImageTweaks import ImageTweaks
import numpy as np
import cv2
from MainTrain import collect_dataset
import MainTrain
import time
import sys


def faceRecognition():
    threshold = 70

    detector = FaceDetector('xml/haarcascade_frontalface_default.xml')
    webcam = VideoCamera()
    images, labels, labels_disc = collect_dataset()
    tweak = ImageTweaks()
    datalbph = MainTrain.get_lbph()

    webcam.start()
    # width = webcam.get_width()
    # height = webcam.get_height()
    # fps = webcam.get_fps()
    # print 'fps: '
    # print fps
    # print 'W: '
    # print width
    # print 'H: '
    # print height

    # outputVid = cv2.VideoWriter('filename.avi', -1, 20.0, (width, height), True)

    # if outputVid.isOpened():
    #   print 'Go '

    cv2.namedWindow("PyData Tutorial", cv2.WINDOW_FULLSCREEN)
    print "Get into The Loop"
    while True:
        frame = webcam.get_frame()
        faces_coord = detector.detect(frame, True)  # detect more than one face
        if len(faces_coord):
            faces = tweak.normalize_faces(frame, faces_coord)  # norm pipeline
            for i, face in enumerate(faces):  # for each detected face
                collector = cv2.face.MinDistancePredictCollector()
                datalbph.predict(face, collector)
                conf = collector.getDist()
                pred = collector.getLabel()
                print "Prediction: " + labels_disc[pred].capitalize() + "\nConfidence: " + str(round(conf))
                if conf < threshold:
                    cv2.putText(frame, labels_disc[pred].capitalize(),
                            (faces_coord[i][0], faces_coord[i][1] - 10),
                            cv2.FONT_HERSHEY_PLAIN, 2, (66, 53, 243), 2)
                else:
                    cv2.putText(frame, "Unknown",
                            (faces_coord[i][0], faces_coord[i][1] - 10),
                            cv2.FONT_HERSHEY_PLAIN, 2, (66, 53, 243), 2)

            tweak.draw_rectangle(frame, faces_coord)  # rectangle around face
        # cv2.putText(frame, "Q to exit", (5, frame.shape[0] - 5),
        #            cv2.FONT_HERSHEY_PLAIN, 1.3, (66, 53, 243), 2, cv2.LINE_AA)
        # save the video if needed
        # outputVid.write(frame)
        cv2.imshow("PyData Tutorial", frame)  # live feed in external

        if cv2.waitKey(1) & 0xFF == 'q':
            cv2.destroyAllWindows()
            break
        if cv2.getWindowProperty("PyData Tutorial", 0) < 0:
            # outputVid.release()
            break
    # outputVid.release()
    cv2.destroyAllWindows()

faceRecognition()
