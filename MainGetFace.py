from VideoCamera import VideoCamera
from FaceDetector import FaceDetector
from ImageTweaks import ImageTweaks
import os
import numpy as np
import cv2


detector = FaceDetector('xml/haarcascade_frontalface_default.xml')
webcam = VideoCamera()
tweak = ImageTweaks()

webcam.start()

folder = "people/" + raw_input('Person: ').lower() # input name
cv2.namedWindow("PyData Tutorial", cv2.WINDOW_AUTOSIZE)

if not os.path.exists(folder):
    os.mkdir(folder)
    counter = 0
    timer = 0
    while counter < 10:  # take 20 pictures
        frame = webcam.get_frame()
        faces_coord = detector.detect(frame)
        # change the condition
        if len(faces_coord):  # every second or so
            faces = tweak.normalize_faces(frame, faces_coord)
            if cv2.waitKey(0) & 0xFF == ord('c'):
                cv2.imwrite(folder + '/' + str(counter) + '.jpg', faces[0])
                counter += 1
                print counter
            tweak.draw_rectangle(frame, faces_coord)
        cv2.imshow("PyData Tutorial", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        timer += 50
    cv2.destroyAllWindows()
else:
    print "This name already exist."

#  and timer % 700 == 50
