import cv2
from threading import Thread


class VideoCamera(object):
     def __init__(self, index=0):
         self.video = cv2.VideoCapture(index)
         _, frame = self.video.read()
         self.index = index
         self.frame = None
         self.stopped = False

         print self.video.isOpened()

     def __del__(self):
         self.video.release()

     def start(self):
         # Thread(target=self.get_frame(), args=()).start()
         return self

     def get_frame(self, in_grayscale=False):
         _, frame = self.video.read()
         if in_grayscale:
             frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
         return frame

     def get_width(self):
         return int(self.video.get(cv2.CAP_PROP_FRAME_WIDTH))

     def get_height(self):
         return int(self.video.get(cv2.CAP_PROP_FRAME_HEIGHT))

     def get_fps(self):
         return int(self.video.get(cv2.CAP_PROP_FPS))
