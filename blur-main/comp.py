import cv2
import psutil
import time
import GPUtil
import numpy as np
from mtcnn import MTCNN

DETECTION_METHOD = "MTCNN"  # "MTCNN" "Haar Cascade" if needed

haar_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
mtcnn_detector = MTCNN() if DETECTION_METHOD == "MTCNN" else None

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

cv2.namedWindow("Face Detection & System Monitor", cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty("Face Detection & System Monitor", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

def get_system_usage():

    cpu_usage = psutil.cpu_percent()
    ram_usage = psutil.virtual_memory().percent
    gpu_usage = 0
    gpu_memory = 0

    gpus = GPUtil.getGPUs()
    if gpus:
        gpu = gpus[0]
        gpu_usage = gpu.load * 100
        gpu_memory = gpu.memoryUsed

    return cpu_usage, ram_usage, gpu_usage, gpu_memory

def process_frame(frame):

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = []

    if DETECTION_METHOD == "Haar Cascade":
        faces = haar_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30))
    elif DETECTION_METHOD == "MTCNN":
        detections = mtcnn_detector.detect_faces(frame)
        faces = [(d['box'][0], d['box'][1], d['box'][2], d['box'][3]) for d in detections]

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    return frame

fps = 0
start_time = time.time()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = process_frame(frame)

    cpu, ram, gpu, gpu_mem = get_system_usage()

    elapsed_time = time.time() - start_time
    fps = 1 / elapsed_time if elapsed_time > 0 else 0
    start_time = time.time()

    info_text = f"Method: {DETECTION_METHOD} | CPU: {cpu:.1f}% | RAM: {ram:.1f}% | GPU: {gpu:.1f}% | FPS: {fps:.1f}"
    cv2.putText(frame, info_text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

    cv2.imshow("Face Detection & System Monitor", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
