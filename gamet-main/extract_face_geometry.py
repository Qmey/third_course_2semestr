import os
import cv2
import mediapipe as mp
import numpy as np
from tqdm import tqdm
import json

INPUT_DIR = "PubFig83"
OUTPUT_DIR = "face_data"

os.makedirs(OUTPUT_DIR, exist_ok=True)

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=True, refine_landmarks=True)

def extract_face_geometry(image_path):
    img = cv2.imread(image_path)
    if img is None:
        return None
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    result = face_mesh.process(rgb)

    if result.multi_face_landmarks:
        face = result.multi_face_landmarks[0]
        return [(lm.x, lm.y, lm.z) for lm in face.landmark]
    return None

data = {}

for person in tqdm(os.listdir(INPUT_DIR)):
    person_path = os.path.join(INPUT_DIR, person)
    if not os.path.isdir(person_path):
        continue

    person_data = []
    for filename in os.listdir(person_path):
        img_path = os.path.join(person_path, filename)
        geometry = extract_face_geometry(img_path)
        if geometry:
            person_data.append(geometry)

    if person_data:
        averaged = np.mean(person_data, axis=0).tolist()
        data[person] = averaged

with open(os.path.join(OUTPUT_DIR, "celebrity_faces.json"), "w") as f:
    json.dump(data, f)

print(f"Сохранено геометрий лиц: {len(data)}")
