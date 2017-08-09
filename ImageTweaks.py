import numpy as np
import cv2
from cv2 import merge


class ImageTweaks:

    def normalize_intensity(self, images):
        images_norms = []
        for image in images:
            is_color = len(image.shape) == 3
            if is_color:
                lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)  # convert to LAB color model
                # split the lab image
                l, a, b = cv2.split(lab)
                # Apply CLAHE to L-channel
                clahe = cv2.createCLAHE(clipLimit=3.0)
                cl = clahe.apply(l)
                image = merge((cl, a, b))
                image = cv2.cvtColor(image, cv2.COLOR_LAB2BGR)  # change back from LAB to BGR
                image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            images_norms.append(cv2.equalizeHist(image))
            # images_norms.append(image)
        return images_norms

    def resize(self, images, size=(150, 150)):
        images_norm = []
        for image in images:
            if image.shape < size:
                image_norm = cv2.resize(image, size,
                                        interpolation=cv2.INTER_AREA)
            else:
                image_norm = cv2.resize(image, size,
                                        interpolation=cv2.INTER_CUBIC)
            images_norm.append(image_norm)
        return images_norm

    def normalize_faces(self, frame, face_coord):
        faces = self.cut_faces(frame, face_coord)
        faces = self.normalize_intensity(faces)
        faces = self.resize(faces)
        return faces

    def draw_rectangle(self, image, coords):
        for(x, y, w, h) in coords:
            w_rm = int(0.3 * w / 2)
            cv2.rectangle(image, (x + w_rm, y), (x + w - w_rm, y + h),
                          (0, 255, 0), 2)

    def cut_faces(self, image, faces_coord):
        faces = []
        for(x, y, w, h) in faces_coord:
            w_rm = int(0.3 * w / 2)
            faces.append(image[y: y + h, x + w_rm: x + w - w_rm])
        return faces
