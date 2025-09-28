import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

hands = mp_hands.Hands(static_image_mode=True, max_num_hands=2)

image = cv2.imread("hand.jpg")
rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

results = hands.process(rgb_image)

if results.multi_hand_landmarks:
    for hand_landmarks in results.multi_hand_landmarks:
        mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

cv2.imshow("Hand Tracking", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
