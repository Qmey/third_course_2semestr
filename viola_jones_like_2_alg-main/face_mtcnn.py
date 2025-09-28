import cv2
from mtcnn import MTCNN

detector = MTCNN()

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    faces = detector.detect_faces(frame_rgb)

    for face in faces:
        x, y, width, height = face["box"]
        keypoints = face["keypoints"]

        cv2.rectangle(frame, (x, y), (x + width, y + height), (0, 255, 0), 2)

        for point in keypoints.values():
            cv2.circle(frame, point, 2, (255, 0, 0), -1)

    cv2.imshow("MTCNN Face Detection (Webcam)", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
