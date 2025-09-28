import cv2
import mediapipe as mp
import numpy as np
import random
import scipy.spatial

mp_face_mesh = mp.solutions.face_mesh

face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1, min_detection_confidence=0.5)

cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = face_mesh.process(rgb_frame)

    h, w, _ = frame.shape
    overlay = frame.copy()
    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:

            landmark_points = [(int(lm.x * w), int(lm.y * h)) for lm in face_landmarks.landmark]

            subdiv = cv2.Subdiv2D((0, 0, w, h))
            for point in landmark_points:
                subdiv.insert(point)
            triangles = subdiv.getTriangleList()
            triangles = np.array(triangles, dtype=np.int32)

            for t in triangles:
                pt1, pt2, pt3 = (t[0], t[1]), (t[2], t[3]), (t[4], t[5])
                pts = np.array([pt1, pt2, pt3], np.int32)

                color = [random.randint(0, 255) for _ in range(3)]

                cv2.fillPoly(overlay, [pts], color)

            nose_x, nose_y = landmark_points[1]
            cv2.circle(frame, (nose_x, nose_y), 20, (0, 0, 255), -1)

        cv2.addWeighted(overlay, 0.5, frame, 0.5, 0, frame)

    cv2.imshow('S', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
