import cv2
import os
import time
import mediapipe as mp
import numpy as np

def run():

    mp_face_mesh = mp.solutions.face_mesh
    face_mesh = mp_face_mesh.FaceMesh(static_image_mode=True)
    drawing_spec = mp.solutions.drawing_utils.DrawingSpec(thickness=1, circle_radius=1)

    DATASET_PATH = "C:/Users/Yerlan/PycharmProjects/Games/games/look_alike/celebrity_photos1"  # <-- путь к папке с подкаталогами

    def extract_landmark_vector(image):
        results = face_mesh.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        if results.multi_face_landmarks:
            landmarks = results.multi_face_landmarks[0].landmark
            return np.array([[l.x, l.y, l.z] for l in landmarks]).flatten()
        return None

    def draw_landmarks(image):
        results = face_mesh.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        if results.multi_face_landmarks:
            annotated_image = image.copy()
            for face_landmarks in results.multi_face_landmarks:
                mp.solutions.drawing_utils.draw_landmarks(
                    image=annotated_image,
                    landmark_list=face_landmarks,
                    connections=mp_face_mesh.FACEMESH_TESSELATION,
                    landmark_drawing_spec=drawing_spec,
                    connection_drawing_spec=drawing_spec)
            return annotated_image
        return image

    def capture_user_face():
        cap = cv2.VideoCapture(0)
        print("3 seconds...")
        time.sleep(3)
        ret, frame = cap.read()
        cap.release()
        if not ret:
            print("ERrore.")
            return None
        return frame

    def find_best_match(user_embedding):
        min_dist = float('inf')
        best_name = None
        best_image = None

        for celeb_name in os.listdir(DATASET_PATH):
            celeb_folder = os.path.join(DATASET_PATH, celeb_name)
            if not os.path.isdir(celeb_folder):
                continue

            for img_name in os.listdir(celeb_folder):
                img_path = os.path.join(celeb_folder, img_name)
                image = cv2.imread(img_path)
                if image is None:
                    continue

                embedding = extract_landmark_vector(image)
                if embedding is None or len(embedding) != len(user_embedding):
                    continue

                dist = np.linalg.norm(user_embedding - embedding)
                if dist < min_dist:
                    min_dist = dist
                    best_name = celeb_name
                    best_image = image.copy()

        return best_name, best_image, min_dist

    def resize_and_convert(img, size):
        img_resized = cv2.resize(img, size)
        if len(img_resized.shape) == 2:
            img_resized = cv2.cvtColor(img_resized, cv2.COLOR_GRAY2BGR)
        return img_resized

    user_frame = capture_user_face()
    if user_frame is None:
        return

    user_embedding = extract_landmark_vector(user_frame)
    if user_embedding is None:
        print("Error.")
        return

    name, celeb_img, distance = find_best_match(user_embedding)
    similarity = max(0, 100 - distance * 50)

    print(f"you look like: {name} about {similarity:.1f}%")

    user_with_landmarks = draw_landmarks(user_frame)
    celeb_with_landmarks = draw_landmarks(celeb_img)

    desired_size = (640, 480)
    user_with_landmarks = resize_and_convert(user_with_landmarks, desired_size)
    celeb_with_landmarks = resize_and_convert(celeb_with_landmarks, desired_size)

    combined = cv2.hconcat([user_with_landmarks, celeb_with_landmarks])
    cv2.imshow("Looks alike?", combined)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    run()
