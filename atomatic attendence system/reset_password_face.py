# reset_password_face.py
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import cv2
import face_recognition
import hashlib
import db

class ResetPasswordFace:
    def __init__(self, root, card_frame, main_app=None):
        self.root = root
        self.card_frame = card_frame
        self.main_app = main_app
        self.detected_uid = None
        self.known_encodings, self.known_ids = db.load_known_faces()
        # Tkinter UI elements
        self.video_label = None
        self.new_pass_entry = None
        self.confirm_pass_entry = None

        # Start face reset process
        self.start_camera_ui()

    # -------------------- CAMERA UI --------------------
    def start_camera_ui(self):
        # Clear previous card
        for widget in self.card_frame.winfo_children():
            widget.destroy()

        # Title and instructions
        Label(self.card_frame, text="Face Verification", font=("Segoe UI", 18, "bold"), bg="white").pack(pady=20)
        Label(self.card_frame, text="Look at the camera 👀", font=("Segoe UI", 12), bg="white").pack(pady=5)
        Label(self.card_frame, text="Press 'Cancel' to exit", font=("Segoe UI", 10, "italic"), bg="white", fg="gray").pack(pady=5)

        # Video frame
        self.video_label = Label(self.card_frame, bg="white")
        self.video_label.pack(pady=10)

        # Cancel button
        Button(self.card_frame, text="Cancel", bg="#E5E7EB", fg="#111827", font=("Segoe UI", 12, "bold"),
               bd=0, pady=8, command=self.stop_camera).pack(pady=10, fill="x", padx=50)

        # Start camera
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            messagebox.showerror("Error", "Cannot access camera")
            return

        self.camera_running = True
        self.update_frame()

    # -------------------- UPDATE FRAME --------------------
    def update_frame(self):
        if not self.camera_running:
            return

        ret, frame = self.cap.read()
        if not ret:
            messagebox.showerror("Camera Error", "Cannot read frame")
            self.stop_camera()
            return

        # Resize for faster recognition
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_frame = small_frame[:, :, ::-1]

        # Face recognition
        faces = face_recognition.face_encodings(rgb_frame)
        if faces:
            for face in faces:
                distances = face_recognition.face_distance(self.known_encodings, face)
                if len(distances) > 0 and min(distances) < 0.45:
                    index = distances.argmin()
                    self.detected_uid = self.known_ids[index]
                    self.camera_running = False
                    self.cap.release()
                    self.video_label.destroy()
                    messagebox.showinfo("Success", f"Face recognized! UID: {self.detected_uid}")
                    self.show_new_password_ui()
                    return

        # Convert frame to Tkinter image
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)
        self.video_label.imgtk = imgtk
        self.video_label.configure(image=imgtk)

        # Repeat after 10 ms
        self.video_label.after(10, self.update_frame)

    # -------------------- STOP CAMERA --------------------
    def stop_camera(self):
        self.camera_running = False
        if hasattr(self, 'cap') and self.cap.isOpened():
            self.cap.release()
        for widget in self.card_frame.winfo_children():
            widget.destroy()
        if self.main_app:
            self.main_app.build_ui()

    # -------------------- NEW PASSWORD UI --------------------
    def show_new_password_ui(self):
        for widget in self.card_frame.winfo_children():
            widget.destroy()

        Label(self.card_frame, text="Set New Password", font=("Segoe UI", 18, "bold"), bg="white").pack(pady=20)
        Label(self.card_frame, text=f"UID: {self.detected_uid}", font=("Segoe UI", 12, "bold"), bg="white", fg="gray").pack(pady=5)

        Label(self.card_frame, text="New Password", font=("Segoe UI", 12), bg="white").pack(pady=5)
        self.new_pass_entry = Entry(self.card_frame, font=("Segoe UI", 12), show="*")
        self.new_pass_entry.pack(pady=5, padx=50, fill="x")

        Label(self.card_frame, text="Confirm Password", font=("Segoe UI", 12), bg="white").pack(pady=5)
        self.confirm_pass_entry = Entry(self.card_frame, font=("Segoe UI", 12), show="*")
        self.confirm_pass_entry.pack(pady=5, padx=50, fill="x")

        Button(self.card_frame, text="Save Password", bg="#2563EB", fg="white", font=("Segoe UI", 12, "bold"),
               bd=0, pady=10, command=self.save_password).pack(pady=20, fill="x", padx=50)

    # -------------------- SAVE PASSWORD --------------------
    def save_password(self):
        p1 = self.new_pass_entry.get().strip()
        p2 = self.confirm_pass_entry.get().strip()
        if not p1 or not p2:
            messagebox.showerror("Error", "Please fill both fields")
            return
        if p1 != p2:
            messagebox.showerror("Error", "Passwords do not match")
            return

        hashed_pwd = hashlib.sha256(p1.encode()).hexdigest()
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE user_registration SET password=%s WHERE unique_id=%s",
                       (hashed_pwd, self.detected_uid))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Password updated successfully")

        if self.main_app:
            self.main_app.build_ui()
        else:
            self.root.destroy()