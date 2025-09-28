import cv2
import mediapipe as mp

mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils

face_mesh = mp_face_mesh.FaceMesh()

image = cv2.imread("face.jpg")
rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

results = face_mesh.process(rgb_image)

if results.multi_face_landmarks:
    for face_landmarks in results.multi_face_landmarks:
        mp_drawing.draw_landmarks(image, face_landmarks, mp_face_mesh.FACEMESH_TESSELATION)

cv2.imshow("Face Mesh", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
