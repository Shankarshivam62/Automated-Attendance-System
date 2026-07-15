# mark_attendance.py
import cv2
import datetime
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import face_recognition
from db import get_connection, mark_attendance

# =========================
# Load faces from DB
# =========================
def load_known_faces():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT unique_id, face_image_path FROM user_registration WHERE face_image_path IS NOT NULL")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    known_encodings = []
    known_unique_ids = []

    for unique_id, face_path in rows:
        print("Trying to load:", face_path)
        try:
            image = face_recognition.load_image_file(face_path)
            encodings = face_recognition.face_encodings(image)
            if encodings:
                known_encodings.append(encodings[0])
                known_unique_ids.append(unique_id)
        except Exception as e:
            print(f"Error loading {face_path}: {e}")

    print(f"Loaded {len(known_unique_ids)} known faces from DB")
    return known_encodings, known_unique_ids

# =========================
# GUI Attendance App
# =========================
class MarkAttendanceApp:
    def __init__(self, parent):
        self.parent = parent
        self.win = Toplevel(self.parent)
        self.win.title("Automatic Attendance - LogFace")
        self.win.attributes("-fullscreen", True)
        self.win.configure(bg="#F3F4F6")

        # Camera
        self.cap = cv2.VideoCapture(0)

        if not self.cap.isOpened():
         messagebox.showerror(
            "Camera Error",
            "Camera not available or already in use.\nPlease check your camera."
        )
         return
        self.running = True

        # Attendance tracking
        self.attendance_marked = set()

        # Load known faces
        self.known_encodings, self.known_unique_ids = load_known_faces()

        # Setup GUI
        self.setup_gui()

        # Start scanning
        self.update_frame()

    # -------------------------
    # GUI setup
    # -------------------------
    def setup_gui(self):
    # ======= TOP BAR =======
        header = Frame(self.win, bg="#111827", height=70)
        header.pack(fill="x")

        Label(
            header,
            text="LogFace • AI Attendance System",
            bg="#111827",
            fg="white",
            font=("Segoe UI", 22, "bold")
        ).pack(side=LEFT, padx=30)

        self.time_label = Label(
            header,
            bg="#111827",
            fg="#9CA3AF",
            font=("Segoe UI", 12)
        )
        self.time_label.pack(side=RIGHT, padx=30)
        self.update_time()

        # ======= MAIN BODY =======
        body = Frame(self.win, bg="#F3F4F6")
        body.pack(fill=BOTH, expand=True, padx=20, pady=20)

        # ======= CAMERA CARD =======
        cam_card = Frame(body, bg="white", bd=0, relief=RIDGE)
        cam_card.pack(side=LEFT, fill=BOTH, expand=True, padx=10)

        Label(
            cam_card,
            text="Live Camera Feed",
            bg="white",
            fg="#111827",
            font=("Segoe UI", 16, "bold")
        ).pack(anchor="w", padx=20, pady=10)

        self.camera_frame = Frame(
            cam_card,
            bg="black",
            width=720,
            height=520
        )
        self.camera_frame.pack(padx=20, pady=10)
        self.camera_frame.pack_propagate(False)

        self.camera_label = Label(self.camera_frame, bg="black")
        self.camera_label.pack(fill=BOTH, expand=True)
        self.camera_label.lift()
        
        # ======= OVERLAY MESSAGE =======
        self.overlay_label = Label(
            cam_card,
            text="",
            bg="#16A34A",
            fg="white",
            font=("Segoe UI", 14, "bold"),
            padx=20,
            pady=8
        )
        self.overlay_label.place(relx=0.5, rely=0.02, anchor=N)
        self.overlay_label.lower()

        # ======= RIGHT PANEL =======
        side = Frame(body, bg="white", width=400)
        side.pack(side=RIGHT, fill=Y, padx=10)
        side.pack_propagate(False)

        Label(
            side,
            text="System Activity",
            bg="white",
            fg="#111827",
            font=("Segoe UI", 16, "bold")
        ).pack(anchor="w", padx=20, pady=10)

        self.log_box = Text(
            side,
            bg="#F9FAFB",
            fg="#111827",
            font=("Segoe UI", 11),
            bd=0
        )
        self.log_box.pack(fill=BOTH, expand=True, padx=20, pady=10)

        self.log_box.insert(END, "✔ System initialized successfully\n")

        Button(
            side,
            text="Exit System",
            bg="#EF4444",
            fg="white",
            font=("Segoe UI", 12, "bold"),
            bd=0,
            padx=20,
            pady=10,
            cursor="hand2",
            command=self.close_window
        ).pack(pady=15)
        # -------------------------
        # Camera frame update
        # -------------------------
    def update_frame(self):
        if not self.running or not self.cap:
            return

        ret, frame = self.cap.read()
        if not ret:
            self.win.after(100, self.update_frame)
            return

        # ================= GUIDE BOX (OpenCV) =================
        cv2.rectangle(frame, (200, 120), (520, 440), (34, 197, 94), 2)
        cv2.putText(
            frame,
            "Align your face inside the box",
            (200, 470),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 255),
            2
        )

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        # Load eye detector
        eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

        # ================= Multiple face check =================
        if len(face_locations) == 0:
            self.overlay_label.lower()  # No face → hide overlay
        elif len(face_locations) > 1:
            # More than 1 face detected → show error
            self.overlay_label.config(
                text="❌ Multiple faces detected! Only one person allowed.",
                bg="#DC2626"
            )
            self.overlay_label.lift()
        else:
            # Only 1 face detected → continue
            (top, right, bottom, left) = face_locations[0]
            face_encoding = face_encodings[0]

            # Crop face for eye detection
            face_gray = cv2.cvtColor(frame[top:bottom, left:right], cv2.COLOR_BGR2GRAY)
            eyes = eye_cascade.detectMultiScale(face_gray, scaleFactor=1.1, minNeighbors=5)

            if len(eyes) == 0:
                # Eyes not detected → show error
                self.overlay_label.config(
                    text="❌ Eyes not detected! Align properly inside the box.",
                    bg="#DC2626"
                )
                self.overlay_label.lift()
            else:
                # Face + eyes detected → check against known faces
                matches = face_recognition.compare_faces(
                    self.known_encodings, face_encoding, tolerance=0.5
                )
                unique_id = "Unknown"

                if True in matches:
                    matched_idx = matches.index(True)
                    unique_id = self.known_unique_ids[matched_idx]

                    if unique_id not in self.attendance_marked:
                        # Try to mark attendance with 1-hour restriction
                        success, msg = mark_attendance(unique_id)

                        if success:
                            self.attendance_marked.add(unique_id)
                            self.overlay_label.config(
                                text=msg,
                                bg="#16A34A"  # Green
                            )
                        else:
                            self.overlay_label.config(
                                text=msg,
                                bg="#DC2626"  # Red
                            )

                        self.overlay_label.lift()
                        self.log_box.insert(
                            END,
                            f"[{datetime.datetime.now().strftime('%H:%M:%S')}] {msg} ({unique_id})\n"
                        )
                        self.log_box.see(END)
                        self.win.after(2000, self.overlay_label.lower)

                # Draw rectangle and label
                color = (0, 255, 0) if unique_id != "Unknown" else (0, 0, 255)
                cv2.rectangle(frame, (left, top), (right, bottom), color, 3)
                cv2.putText(
                    frame,
                    unique_id,
                    (left, top - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                    (255, 255, 255), 2
                )

        # Update Tkinter camera image
        img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        imgtk = ImageTk.PhotoImage(image=img)
        self.camera_label.imgtk = imgtk
        self.camera_label.configure(image=imgtk)

        # Repeat every 30ms
        self.win.after(30, self.update_frame)

    # -------------------------
    # Close window
    # -------------------------
    def close_window(self):
        self.running = False
        if self.cap:
            self.cap.release()
        self.win.destroy()
        
        
        
    def update_time(self):
        now = datetime.datetime.now().strftime("%d %b %Y | %H:%M:%S")
        self.time_label.config(text=now)
        self.win.after(1000, self.update_time)