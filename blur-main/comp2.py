import cv2
import psutil
import time
import numpy as np
import matplotlib.pyplot as plt
from mtcnn import MTCNN
from matplotlib.animation import FuncAnimation

haar_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
mtcnn_detector = MTCNN()

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

data = {"method": [], "cpu": [], "ram": [], "fps": []}
methods = ["Haar Cascade", "MTCNN"]
current_method = 0

fig, axes = plt.subplots(3, 1, figsize=(8, 6))
fig.suptitle("Face Detection Performance Comparison")


def detect_faces(frame, method):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    if method == "Haar Cascade":
        faces = haar_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30))
    else:
        detections = mtcnn_detector.detect_faces(frame)
        faces = [(d['box'][0], d['box'][1], d['box'][2], d['box'][3]) for d in detections]
    return faces


def update(frame):
    global current_method
    method = methods[current_method]
    ret, frame = cap.read()
    if not ret:
        return

    start_time = time.time()
    detect_faces(frame, method)
    fps = 1 / (time.time() - start_time)

    cpu_usage = psutil.cpu_percent()
    ram_usage = psutil.virtual_memory().percent

    data["method"].append(method)
    data["cpu"].append(cpu_usage)
    data["ram"].append(ram_usage)
    data["fps"].append(fps)

    if len(data["cpu"]) > 50:
        for key in data:
            data[key].pop(0)

    axes[0].cla()
    axes[1].cla()
    axes[2].cla()

    axes[0].set_title("CPU Usage (%)")
    axes[1].set_title("RAM Usage (%)")
    axes[2].set_title("FPS")

    colors = ["red" if m == "MTCNN" else "blue" for m in data["method"]]

    axes[0].bar(range(len(data["cpu"])), data["cpu"], color=colors)
    axes[1].bar(range(len(data["ram"])), data["ram"], color=colors)
    axes[2].bar(range(len(data["fps"])), data["fps"], color=colors)

    current_method = 1 - current_method


ani = FuncAnimation(fig, update, interval=500)
plt.show()
cap.release()
cv2.destroyAllWindows()
