import cv2
import mediapipe as mp

mp_objectron = mp.solutions.objectron
mp_drawing = mp.solutions.drawing_utils

objectron = mp_objectron.Objectron(static_image_mode=True, max_num_objects=1, model_name='Shoe')

image = cv2.imread("shoe.jpg")
rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

results = objectron.process(rgb_image)

if results.detected_objects:
    for obj in results.detected_objects:
        mp_drawing.draw_landmarks(image, obj.landmarks_2d, mp_objectron.BOX_CONNECTIONS)

cv2.imshow("Objectron 3D Tracking", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
