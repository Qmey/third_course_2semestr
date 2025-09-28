import sys
import cv2
import numpy as np
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget, QComboBox
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QImage, QPixmap
from deepface import DeepFace
from mtcnn import MTCNN


class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(QImage)

    def __init__(self, blur_mode="GaussianBlur", detection_method="Haar Cascade"):
        super().__init__()
        self._run_flag = True
        self.blur_mode = blur_mode
        self.detection_method = detection_method
        self.emoji = cv2.imread("neutral.jpg", cv2.IMREAD_UNCHANGED)
        self.detector_haar = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.detector_mtcnn = MTCNN()

    def run(self):
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

        while self._run_flag:
            ret, frame = cap.read()
            if not ret:
                continue

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            if self.detection_method == "Haar Cascade":
                faces = self.detector_haar.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30))
            elif self.detection_method == "MTCNN":
                faces_mtcnn = self.detector_mtcnn.detect_faces(frame)
                faces = [(d['box'][0], d['box'][1], d['box'][2], d['box'][3]) for d in faces_mtcnn]
            else:
                faces = []

            for (x, y, w, h) in faces:
                face = frame[y:y + h, x:x + w]

                if self.blur_mode == "Emoji":
                    try:
                        emotion_analysis = DeepFace.analyze(face, actions=['emotion'], enforce_detection=False)
                        dominant_emotion = emotion_analysis[0]['dominant_emotion']

                        emoji_dict = {
                            "happy": "happy.jpg",
                            "angry": "angry.jpg",
                            "surprise": "surprised.jpeg",
                            "sad": "sad.jpg",
                            "neutral": "neutral.jpg"
                        }

                        if dominant_emotion in emoji_dict:
                            self.emoji = cv2.imread(emoji_dict[dominant_emotion], cv2.IMREAD_UNCHANGED)
                    except:
                        pass

                    emoji_resized = cv2.resize(self.emoji, (w, h))
                    blurred_face = emoji_resized[:, :, :3]
                elif self.blur_mode == "GaussianBlur":
                    blurred_face = cv2.GaussianBlur(face, (51, 51), 30)
                elif self.blur_mode == "Pixelation":
                    blurred_face = cv2.resize(face, (10, 10), interpolation=cv2.INTER_LINEAR)
                    blurred_face = cv2.resize(blurred_face, (w, h), interpolation=cv2.INTER_NEAREST)
                elif self.blur_mode == "Black Box":
                    blurred_face = np.zeros_like(face)
                elif self.blur_mode == "Grayscale Mask":
                    blurred_face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
                    blurred_face = cv2.cvtColor(blurred_face, cv2.COLOR_GRAY2BGR)
                elif self.blur_mode == "Warping":
                    M = np.float32([[1, -0.5, 0], [-0.5, 1, 0]])
                    blurred_face = cv2.warpAffine(face, M, (w, h))
                elif self.blur_mode == "Blur Ring":
                    blurred_face = cv2.GaussianBlur(face, (51, 51), 30)
                    center_mask = np.zeros_like(face, dtype=np.uint8)
                    cv2.circle(center_mask, (w // 2, h // 2), min(w, h) // 4, (1, 1, 1), -1)
                    blurred_face = (face * center_mask) + (blurred_face * (1 - center_mask))
                else:
                    blurred_face = face

                frame[y:y + h, x:x + w] = blurred_face

            rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_image.shape
            bytes_per_line = ch * w
            qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
            self.change_pixmap_signal.emit(qt_image)

        cap.release()

    def stop(self):
        self._run_flag = False
        self.wait()

    def set_blur_mode(self, mode):
        self.blur_mode = mode

    def set_detection_method(self, method):
        self.detection_method = method


class FaceBlurApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Face Blur App')

        self.showMaximized()
        self.setGeometry(100, 100, 800, 600)

        self.video_label = QLabel(self)
        self.video_label.setFixedSize(1920, 1080)

        self.start_button = QPushButton('Запуск', self)
        self.start_button.clicked.connect(self.start_video)

        self.stop_button = QPushButton('Остановить', self)
        self.stop_button.clicked.connect(self.stop_video)

        self.blur_mode_selector = QComboBox(self)
        self.blur_mode_selector.addItems(
            ["GaussianBlur", "Pixelation", "Black Box", "Grayscale Mask", "Emoji", "Warping",
             "Blur Ring"])
        self.blur_mode_selector.currentTextChanged.connect(self.change_blur_mode)

        self.detection_method_selector = QComboBox(self)
        self.detection_method_selector.addItems(["Haar Cascade", "MTCNN"])
        self.detection_method_selector.currentTextChanged.connect(self.change_detection_method)

        layout = QVBoxLayout()
        layout.addWidget(self.video_label)
        layout.addWidget(self.blur_mode_selector)
        layout.addWidget(self.detection_method_selector)
        layout.addWidget(self.start_button)
        layout.addWidget(self.stop_button)
        self.setLayout(layout)

        self.thread = VideoThread()
        self.thread.change_pixmap_signal.connect(self.update_image)

    def start_video(self):
        self.thread.start()

    def stop_video(self):
        self.thread.stop()
        self.video_label.clear()
        self.video_label.setText("Видео остановлено")

    def change_blur_mode(self, mode):
        self.thread.set_blur_mode(mode)

    def change_detection_method(self, method):
        self.thread.set_detection_method(method)

    def update_image(self, qt_image):
        self.video_label.setPixmap(QPixmap.fromImage(qt_image))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = FaceBlurApp()
    main_window.show()
    sys.exit(app.exec_())
