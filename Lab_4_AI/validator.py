import cv2
import os
import tkinter as tk
from tkinter import filedialog
import numpy as np


class PassportPhotoValidator:
    def __init__(self, photo_path):
        self.photo = cv2.imread(photo_path)
        self.gray_photo = cv2.cvtColor(self.photo, cv2.COLOR_BGR2GRAY)

    def is_color_photo(self):
        return not (self.gray_photo.std() < 1)

    def is_portrait_or_square(self):
        aspect_ratio = self.photo.shape[1] / self.photo.shape[0]
        return 0.77 <= aspect_ratio <= 1.3

    def is_one_person(self):
        face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        faces = face_cascade.detectMultiScale(self.gray_photo, scaleFactor=1.3, minNeighbors=5)
        return len(faces) == 1

    def is_eyes_at_same_level(self):
        face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        faces = face_cascade.detectMultiScale(self.gray_photo, scaleFactor=1.3, minNeighbors=5)

        if len(faces) == 1:
            (x, y, w, h) = faces[0]

            # Get the region of interest for the eyes
            roi_gray = self.gray_photo[y:y + h, x:x + w]
            eyes_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
            eyes = eyes_cascade.detectMultiScale(roi_gray)

            if len(eyes) == 2:
                # Check that the eyes are at the same level with a max error of 5 pixels
                y1 = eyes[0][1] + eyes[0][3] / 2
                y2 = eyes[1][1] + eyes[1][3] / 2
                return abs(y1 - y2) <= 5

        return False

    def is_head_area_valid(self):
        face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        faces = face_cascade.detectMultiScale(self.gray_photo, scaleFactor=1.3, minNeighbors=5)

        if len(faces) == 1:
            (x, y, w, h) = faces[0]

            # Calculate the area of the head
            head_area = w * h

            # Calculate the area of the photo
            photo_area = self.photo.shape[0] * self.photo.shape[1]

            # Check that the head area is between 20% to 50% of the photo area
            return 0.2 * photo_area <= head_area <= 0.5 * photo_area

        return False

    def is_valid_passport_photo(self):
        return (self.is_color_photo() and self.is_portrait_or_square()
                and self.is_one_person() and self.is_eyes_at_same_level()
                and self.is_head_area_valid())
