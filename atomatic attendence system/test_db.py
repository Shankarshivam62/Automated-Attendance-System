
# from mark_attendance import load_known_faces

# encodings, ids = load_known_faces()
# print("Faces loaded:", len(encodings))
# print("User IDs:", ids)
# import db

# print(hasattr(db, "user_exists"))
# print(hasattr(db, "email_exists"))
# print(hasattr(db, "phone_exists"))
# print(hasattr(db, "save_user_to_db"))
# print(hasattr(db, "mark_attendance"))

# import db

# print("update_face_path exists:", hasattr(db, "update_face_path"))
from attendance_details import AttendanceDetailsPage
print("IMPORT OK")
import db
print(db.get_attendance_by_date("your_id"))
