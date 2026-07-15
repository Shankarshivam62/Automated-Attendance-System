from deepface import DeepFace
import os
import cv2
import numpy as np

DATASET_PATH = "face_dataset"

# Store embeddings
known_faces = {}
model_name = "Facenet"

def load_faces():
    global known_faces

    for user_id in os.listdir(DATASET_PATH):
        user_path = os.path.join(DATASET_PATH, user_id)

        if not os.path.isdir(user_path):
            continue

        embeddings = []

        for img_name in os.listdir(user_path):
            img_path = os.path.join(user_path, img_name)

            try:
                embedding = DeepFace.represent(
                    img_path=img_path,
                    model_name=model_name,
                    enforce_detection=False
                )[0]["embedding"]

                embeddings.append(embedding)

            except:
                pass

        if embeddings:
            known_faces[user_id] = embeddings

    print("✅ Faces Loaded:", len(known_faces))


def recognize_face_fast(frame):
    try:
        embedding = DeepFace.represent(
            img_path=frame,
            model_name=model_name,
            enforce_detection=False
        )[0]["embedding"]

        best_match = None
        min_distance = float("inf")

        for user_id, embeds in known_faces.items():
            for e in embeds:
                dist = np.linalg.norm(np.array(e) - np.array(embedding))

                if dist < min_distance:
                    min_distance = dist
                    best_match = user_id

        # Threshold (IMPORTANT)
        if min_distance < 10:
            return best_match

        return None

    except Exception as e:
        print("Error:", e)
        return None