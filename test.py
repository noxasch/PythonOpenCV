# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'test.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!
from VideoCamera import VideoCamera
from FaceDetector import FaceDetector
from ImageTweaks import ImageTweaks
import numpy as np
import cv2
from MainTrain import collect_dataset
import MainTrain
import time
import sys
import os
from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("Administrator Panel"))
        MainWindow.setFixedSize(482, 197)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.stop_btn = QtGui.QPushButton(self.centralwidget)
        self.stop_btn.setGeometry(QtCore.QRect(370, 100, 75, 23))
        self.stop_btn.setObjectName(_fromUtf8("stop_btn"))
        self.groupBox = QtGui.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(10, 10, 321, 161))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.add_person_btn = QtGui.QPushButton(self.groupBox)
        self.add_person_btn.setGeometry(QtCore.QRect(30, 30, 111, 23))
        self.add_person_btn.setObjectName(_fromUtf8("add_person_btn"))
        self.capture_btn = QtGui.QPushButton(self.groupBox)
        self.capture_btn.setGeometry(QtCore.QRect(220, 30, 75, 23))
        self.capture_btn.setObjectName(_fromUtf8("capture_btn"))
        self.finish_btn = QtGui.QPushButton(self.groupBox)
        self.finish_btn.setGeometry(QtCore.QRect(220, 60, 75, 23))
        self.finish_btn.setObjectName(_fromUtf8("finish_btn"))
        self.start_btn = QtGui.QPushButton(self.centralwidget)
        self.start_btn.setGeometry(QtCore.QRect(370, 60, 75, 23))
        self.start_btn.setObjectName(_fromUtf8("start_btn"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 482, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        ##
        ##
        ##
        ##

        self.disable_buttons()

        self.add_person_btn.clicked.connect(self.enable_buttons)
        self.finish_btn.clicked.connect(self.disable_buttons)

        self.start_btn.clicked.connect(self.faceRecognition)

        self.stop_btn.clicked.connect(self.close_facerec)

        ##
        ##
        ##
        ##
        ##
        ##
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("Administrator Panel", "Administrator Panel", None))
        self.stop_btn.setText(_translate("MainWindow", "Stop", None))
        self.groupBox.setTitle(_translate("MainWindow", "GroupBox", None))
        self.add_person_btn.setText(_translate("MainWindow", "Add New Person", None))
        self.capture_btn.setText(_translate("MainWindow", "Capture", None))
        self.finish_btn.setText(_translate("MainWindow", "Finish", None))
        self.start_btn.setText(_translate("MainWindow", "Start", None))

    def enable_buttons(self):
        self.capture_btn.setDisabled(False)
        self.finish_btn.setDisabled(False)

    def disable_buttons(self):
        self.capture_btn.setDisabled(True)
        self.finish_btn.setDisabled(True)

    def faceRecognition(self):
        threshold = 70

        detector = FaceDetector('xml/haarcascade_frontalface_default.xml')
        webcam = VideoCamera()
        images, labels, labels_disc = collect_dataset()
        tweak = ImageTweaks()
        datalbph = MainTrain.get_lbph()


        width = webcam.get_width()
        height = webcam.get_height()
        fps = webcam.get_fps()
        print 'fps: '
        print fps
        print 'W: '
        print width
        print 'H: '
        print height

        # outputVid = cv2.VideoWriter('filename.avi', -1, 20.0, (width, height), True)

        # if outputVid.isOpened():
        #   print 'Go '

        cv2.namedWindow("PyData Tutorial", cv2.WINDOW_FULLSCREEN)
        cv2.startWindowThread()
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

    def close_facerec(self):
        cv2.destroyWindow("PyData Tutorial")

    def GetFace(self):
        detector = FaceDetector('xml/haarcascade_frontalface_default.xml')
        webcam = VideoCamera()
        tweak = ImageTweaks()

        folder = "people/" + raw_input('Person: ').lower() # input name
        cv2.namedWindow("PyData Tutorial", cv2.WINDOW_AUTOSIZE)

        if not os.path.exists(folder):
            os.mkdir(folder)
            counter = 0
            timer = 0
            while counter < 10:  # take 20 pictures
                frame = webcam.get_frame()
                faces_coord = detector.detect(frame)
                if len(faces_coord) and timer % 700 == 50:  # every second or so
                    faces = tweak.normalize_faces(frame, faces_coord)
                    cv2.imwrite(folder + '/' + str(counter) + '.jpg', faces[0])
                    # clear_output(wait=True)
                    # print("IM IN THE IF")
                    counter += 1
                    print counter
                # print("NOT IN THE IF")
                tweak.draw_rectangle(frame, faces_coord)
                cv2.imshow("PyData Tutorial", frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                timer += 50
            cv2.destroyAllWindows()
        else:
            print "This name already exist."

# This is the main function
if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

