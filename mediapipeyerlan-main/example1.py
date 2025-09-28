import cv2
import mediapipe as mp

mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils

face_detection = mp_face_detection.FaceDetection()

image = cv2.imread("face.jpg")
rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

results = face_detection.process(rgb_image)

if results.detections:
    for detection in results.detections:
        mp_drawing.draw_detection(image, detection)

cv2.imshow("Face Detection", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
