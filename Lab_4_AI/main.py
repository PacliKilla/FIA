import os
import cv2
from PyQt5 import QtCore, QtGui, QtWidgets

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
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        faces = face_cascade.detectMultiScale(self.gray_photo, scaleFactor=1.3, minNeighbors=5)
        return len(faces) == 1

    def is_eyes_at_same_level(self):
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        faces = face_cascade.detectMultiScale(self.gray_photo, scaleFactor=1.3, minNeighbors=5)

        if len(faces) == 1:
            (x, y, w, h) = faces[0]

            # Get the region of interest for the eyes
            roi_gray = self.gray_photo[y:y + h, x:x + w]
            eyes_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
            eyes = eyes_cascade.detectMultiScale(roi_gray)

            if len(eyes) == 2:
                # Check that the eyes are at the same level with a max error of 5 pixels
                y1 = eyes[0][1] + eyes[0][3] / 2
                y2 = eyes[1][1] + eyes[1][3] / 2
                return abs(y1 - y2) <= 5

        return False

    def is_head_area_valid(self):
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
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


class FaceDetector(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Face Detector")

        # Create the main widget and layout
        self.main_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.main_widget)
        self.layout = QtWidgets.QVBoxLayout(self.main_widget)

        # Create the photo label and browse button
        self.photo_label = QtWidgets.QLabel(self)
        self.photo_label.setAlignment(QtCore.Qt.AlignCenter)
        self.layout.addWidget(self.photo_label)

        self.browse_button = QtWidgets.QPushButton("Browse", self)
        self.browse_button.clicked.connect(self.browse_photo)
        self.layout.addWidget(self.browse_button)

        # Create the detect button
        self.detect_button = QtWidgets.QPushButton("Detect", self)
        self.detect_button.clicked.connect(self.detect_faces)
        self.detect_button.setEnabled(False)
        self.layout.addWidget(self.detect_button)

    def browse_photo(self):
        # Open a file dialog to select a photo
        file_dialog = QtWidgets.QFileDialog(self)
        file_dialog.setNameFilter("Images (*.jpg *.jpeg *.png)")
        file_dialog.setFileMode(QtWidgets.QFileDialog.ExistingFile)
        file_dialog.setViewMode(QtWidgets.QFileDialog.Detail)
        if file_dialog.exec_() == QtWidgets.QDialog.Accepted:
            self.file_path = file_dialog.selectedFiles()[0]
            self.photo = cv2.imread(self.file_path)
            self.display_photo()
            self.detect_button.setEnabled(True)

    def display_photo(self):
        # Convert the photo from BGR to RGB color space
        photo_rgb = cv2.cvtColor(self.photo, cv2.COLOR_BGR2RGB)

        # Convert the photo to a QImage and display it in the photo label
        q_img = QtGui.QImage(photo_rgb.data, photo_rgb.shape[1], photo_rgb.shape[0], photo_rgb.shape[1] * 3,
                             QtGui.QImage.Format_RGB888)
        q_pixmap = QtGui.QPixmap.fromImage(q_img)
        self.photo_label.setPixmap(q_pixmap)

    def detect_faces(self):
        # Convert the photo to grayscale and detect faces using Haar cascades
        gray = cv2.cvtColor(self.photo, cv2.COLOR_BGR2GRAY)
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        # Draw rectangles around the detected faces
        for (x, y, w, h) in faces:
            cv2.rectangle(self.photo, (x, y), (x+w, y+h), (0, 255, 0), 2)

        # Display the photo with the detected faces
        self.display_photo()

        # Check if the photo is a valid passport photo
        validator = PassportPhotoValidator(self.file_path)
        is_valid = validator.is_valid_passport_photo()

        # Show the result
        if is_valid:
            QtWidgets.QMessageBox.information(self, "Result", "Valid passport photo.")
        else:
            QtWidgets.QMessageBox.warning(self, "Result", "Not a valid passport photo.")

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    detector = FaceDetector()
    detector.show()
    app.exec_()