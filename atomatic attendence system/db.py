import mysql.connector
import datetime
import face_recognition
import os
# =========================
# DATABASE CONFIG
# =========================
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "Sitaram620@",
    "database": "logface"
}

# =========================
# CONNECTION
# =========================
def get_connection():
    return mysql.connector.connect(**DB_CONFIG)

# =========================
# CHECK USER EXISTS
# =========================
def user_exists(unique_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT 1 FROM user_registration WHERE unique_id = %s",
        (unique_id,)
    )
    exists = cursor.fetchone() is not None
    cursor.close()
    conn.close()
    return exists

# =========================
# CHECK EMAIL EXISTS
# =========================
def email_exists(email):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT 1 FROM user_registration WHERE email = %s",
        (email,)
    )
    exists = cursor.fetchone() is not None
    cursor.close()
    conn.close()
    return exists

# =========================
# CHECK PHONE EXISTS
# =========================
def phone_exists(phone):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT 1 FROM user_registration WHERE phone = %s",
        (phone,)
    )
    exists = cursor.fetchone() is not None
    cursor.close()
    conn.close()
    return exists

# =========================
# SAVE USER REGISTRATION
# =========================
def save_user_to_db(
    unique_id,
    first_name,
    middle_name,
    last_name,
    email,
    phone,
    password,
    face_path=None
):
    if user_exists(unique_id):
        return False, "❌ Unique ID already exists"

    if email_exists(email):
        return False, "❌ Email already exists"

    if phone_exists(phone):
        return False, "❌ Phone number already exists"

    conn = get_connection()
    cursor = conn.cursor()

    if middle_name == "":
        middle_name = None

    sql = """
    INSERT INTO user_registration
    (unique_id, first_name, middle_name, last_name, email, phone, password, face_image_path, registered_at)
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """

    data = (
        unique_id,
        first_name,
        middle_name,
        last_name,
        email,
        phone,
        password,
        face_path,
        datetime.datetime.now()
    )

    try:
        cursor.execute(sql, data)
        conn.commit()
        return True, "✅ Registration successful"
    except Exception as e:
        return False, f"❌ Database Error: {e}"
    finally:
        cursor.close()
        conn.close()

# MARK ATTENDANCE (1-Hour Check)
# =========================
def mark_attendance(unique_id):
    """
    Marks attendance for the given user.
    If the user already marked attendance within 1 hour, returns False with a message.
    """
    conn = get_connection()
    cursor = conn.cursor()
    now = datetime.datetime.now()
    one_hour_ago = now - datetime.timedelta(hours=1)

    # Check if user has already marked attendance within the last 1 hour
    cursor.execute(
        """
        SELECT marked_at 
        FROM attendance_logs 
        WHERE unique_id=%s 
        ORDER BY marked_at DESC 
        LIMIT 1
        """,
        (unique_id,)
    )
    row = cursor.fetchone()
    if row:
        last_marked = row[0]
        if last_marked >= one_hour_ago:
            cursor.close()
            conn.close()
            return False, "❌ Attendance already marked within 1 hour"

    # Insert new attendance record
    cursor.execute(
        """
        INSERT INTO attendance_logs (unique_id, marked_at, attendance_date)
        VALUES (%s, %s, %s)
        """,
        (unique_id, now, now.date())
    )
    conn.commit()
    cursor.close()
    conn.close()
    return True, "✔ Attendance marked successfully"

def update_face_path(unique_id, face_image_path):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE user_registration SET face_image_path=%s WHERE unique_id=%s",
        (face_image_path, unique_id)
    )
    conn.commit()
    cursor.close()
    conn.close()
    


def is_face_duplicate(new_face_path, threshold=0.45):
    """
    Returns True if face already exists in DB
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute( "SELECT face_image_path FROM user_registration WHERE face_image_path IS NOT NULL")
    records = cursor.fetchall()

    new_img = face_recognition.load_image_file(new_face_path)
    new_enc = face_recognition.face_encodings(new_img)
    if not new_enc:
        return False
    new_enc = new_enc[0]
    for (path,) in records:
        if not path or not os.path.exists(path):
            continue
        old_img = face_recognition.load_image_file(path)
        old_enc = face_recognition.face_encodings(old_img)
        if not old_enc:
            continue
        distance = face_recognition.face_distance([old_enc[0]], new_enc)[0]
        if distance < threshold:
            return True
    return False
def cleanup_orphan_faces():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT face_path FROM user_registration WHERE face_path IS NOT NULL")
    valid_faces = {row[0] for row in cursor.fetchall()}

    faces_dir = "faces"
    if not os.path.exists(faces_dir):
        return

    for file in os.listdir(faces_dir):
        path = os.path.join(faces_dir, file)
        if path not in valid_faces:
            try:
                os.remove(path)
            except:
                pass
def load_known_faces():
    """
    Load all known face encodings from database
    Returns:
        known_encodings: list
        known_ids: list
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT unique_id, face_image_path
        FROM user_registration
        WHERE face_image_path IS NOT NULL
    """)

    known_encodings = []
    known_ids = []

    for unique_id, path in cursor.fetchall():
        if not path or not os.path.exists(path):
            continue

        image = face_recognition.load_image_file(path)
        encodings = face_recognition.face_encodings(image)

        if encodings:
            known_encodings.append(encodings[0])
            known_ids.append(unique_id)

    cursor.close()
    conn.close()

    return known_encodings, known_ids

def load_known_faces():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT unique_id, face_image_path
        FROM user_registration
        WHERE face_image_path IS NOT NULL
    """)

    known_encodings = []
    known_ids = []

    for unique_id, path in cursor.fetchall():
        if not path or not os.path.exists(path):
            continue

        image = face_recognition.load_image_file(path)
        encodings = face_recognition.face_encodings(image)

        if encodings:
            known_encodings.append(encodings[0])
            known_ids.append(unique_id)

    cursor.close()
    conn.close()
    return known_encodings, known_ids

def get_attendance_stats(unique_id):
    conn = get_connection()
    cursor = conn.cursor()

    # Total unique days user attended
    cursor.execute("""
        SELECT COUNT(DISTINCT attendance_date)
        FROM attendance_logs
        WHERE unique_id = %s
    """, (unique_id,))
    present_days = cursor.fetchone()[0] or 0

    # Total days since registration
    cursor.execute("""
        SELECT DATEDIFF(CURDATE(), registered_at)
        FROM user_registration
        WHERE unique_id = %s
    """, (unique_id,))
    total_days = cursor.fetchone()[0] or 1

    cursor.close()
    conn.close()

    percentage = (present_days / total_days) * 100 if total_days > 0 else 0

    return {
        "present_days": present_days,
        "total_days": total_days,
        "percentage": round(percentage, 2)
    }
def get_attendance_summary(unique_id):
    conn = get_connection()
    cursor = conn.cursor()

    # Present days
    cursor.execute("""
        SELECT COUNT(DISTINCT attendance_date)
        FROM attendance_logs
        WHERE unique_id=%s
    """, (unique_id,))
    present = cursor.fetchone()[0] or 0

    # Total days
    cursor.execute("""
        SELECT DATEDIFF(CURDATE(), registered_at)
        FROM user_registration
        WHERE unique_id=%s
    """, (unique_id,))
    total = cursor.fetchone()[0] or 1

    absent = total - present if total > present else 0

    cursor.close()
    conn.close()

    return present, absent

def get_attendance_by_date(unique_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT attendance_date
        FROM attendance_logs
        WHERE unique_id = %s
        ORDER BY attendance_date
    """, (unique_id,))

    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return [row[0] for row in data]

def update_password(unique_id, new_password):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE user_registration SET password=%s WHERE unique_id=%s",
                   (new_password, unique_id))
    conn.commit()
    cursor.close()
    conn.close()
    
def get_user_by_id(uid):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_registration WHERE unique_id=%s", (uid,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user