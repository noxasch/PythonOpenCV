import numpy as np
import os
import cv2
import cv2.face


def collect_dataset():
    images = []
    labels = []
    labels_disc = {}
    people = [person for person in os.listdir("people/")]
    for i, person in enumerate(people):
        labels_disc[i] = person
        for image in os.listdir("people/" + person):
            images.append(cv2.imread("people/" + person + '/' + image,
                                     0))
            labels.append(i)
    return images, np.array(labels), labels_disc

images, labels, labels_disc = collect_dataset()

# rec_eig = cv2.face.createEigenFaceRecognizer()
# rec_eig.train(images, labels)


# rec_fisher = cv2.face.createFisherFaceRecognizer()
# rec_fisher.train(images, labels)

rec_lbph = cv2.face.createLBPHFaceRecognizer()
rec_lbph.train(images, labels)


def get_lbph():
    return rec_lbph


