import cv2
import mediapipe as mp

mp_holistic = mp.solutions.holistic
mp_drawing = mp.solutions.drawing_utils

holistic = mp_holistic.Holistic()

image = cv2.imread("person.png")
rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

results = holistic.process(rgb_image)

if results.face_landmarks:
    mp_drawing.draw_landmarks(image, results.face_landmarks, mp_holistic.FACEMESH_TESSELATION)

if results.pose_landmarks:
    mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS)

if results.left_hand_landmarks:
    mp_drawing.draw_landmarks(image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS)

if results.right_hand_landmarks:
    mp_drawing.draw_landmarks(image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS)

cv2.imshow("Holistic Tracking", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
