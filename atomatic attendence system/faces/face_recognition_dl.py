from deepface import DeepFace
import cv2
import os
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
DATASET_PATH = "face_dataset"

def recognize_face_dl(frame):
    try:
        temp_path = "temp.jpg"
        cv2.imwrite(temp_path, frame)

        result = DeepFace.find(
            img_path=temp_path,
            db_path=DATASET_PATH,
            model_name="Facenet",
            enforce_detection=False
        )

        if len(result) > 0 and not result[0].empty:
            matched_path = result[0].iloc[0]['identity']
            user_id = os.path.basename(os.path.dirname(matched_path))
            return user_id

        return None

    except Exception as e:
        print("Error:", e)
        return None