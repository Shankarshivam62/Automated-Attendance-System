from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
import smtplib
from email.message import EmailMessage
import face_recognition
from db import get_connection, user_exists, load_known_faces
import hashlib
import random
import string
from face_login_ui import FaceLoginUI

# ------------------------- Helpers -------------------------
def generate_password(length=10):
    chars = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(random.choice(chars) for _ in range(length))

def send_email(to_email, subject, body, from_email="youremail@gmail.com", app_password="your_app_password"):
    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_email, app_password)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        messagebox.showerror("Email Error", str(e))
        return False

# ------------------------- Forgot Password UI -------------------------
class ForgotPasswordApp(Frame):
    def __init__(self, root, main_app=None):
        super().__init__(root)
        self.root = root
        self.main_app = main_app
        self.build_ui()
        self.place(relwidth=1, relheight=1)

    def build_ui(self):
        self.config(bg="#f0f2f5")

        # Center card
        self.card = Frame(self, bg="white", bd=0, relief="ridge")
        self.card.place(relx=0.5, rely=0.5, anchor="center", width=450, height=500)

        Label(self.card, text="🔑 Reset Password", bg="white", fg="#111827", font=("Segoe UI", 22, "bold")).pack(pady=20)

        # Unique ID input
        self.uid_entry = self.create_input(self.card, "Unique ID").pack(pady=(10, 5))
        # Email input
        self.email_entry = self.create_input(self.card, "Registered Email").pack(pady=(5, 15))

        # Reset via Email
        Button(
            self.card, text="📩 Reset via Email",
            bg="#2563EB", fg="white",
            font=("Segoe UI", 12, "bold"),
            bd=0, pady=12, cursor="hand2",
            command=self.reset_via_email
        ).pack(padx=40, pady=10, fill="x")

        # Reset via Face
        Button(
            self.card, text="👤 Reset via Face",
            bg="#10B981", fg="white",
            font=("Segoe UI", 12, "bold"),
            bd=0, pady=12, cursor="hand2",
            command=self.reset_via_face
        ).pack(padx=40, pady=10, fill="x")

        # Back button
        Button(
            self.card, text="← Back to Login",
            bg="#E5E7EB", fg="#111827",
            font=("Segoe UI", 12),
            bd=0, pady=10, cursor="hand2",
            command=self.return_to_login
        ).pack(padx=40, pady=20, fill="x")

    def create_input(self, parent, placeholder):
        frame = Frame(parent, bg="#f3f4f6", bd=1, relief="solid")
        frame.pack(pady=10, padx=40, fill="x")
        entry = Entry(frame, font=("Segoe UI", 12), bd=0, fg="#6B7280")
        entry.pack(ipady=8, fill="x", padx=10)
        entry.insert(0, placeholder)

        def clear_placeholder(event):
            if entry.get() == placeholder:
                entry.delete(0, END)
                entry.config(fg="#111827")

        def add_placeholder(event):
            if not entry.get():
                entry.insert(0, placeholder)
                entry.config(fg="#6B7280")

        entry.bind("<FocusIn>", clear_placeholder)
        entry.bind("<FocusOut>", add_placeholder)
        return entry

    # ================= Email Reset =================
    def reset_via_email(self):
        uid = self.uid_entry.get().strip()
        email = self.email_entry.get().strip()
        if not user_exists(uid):
            messagebox.showerror("Error", "User ID not found")
            return

        temp_password = generate_password()
        hashed_pwd = hashlib.sha256(temp_password.encode()).hexdigest()

        # Update DB
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE user_registration SET password=%s WHERE unique_id=%s", (hashed_pwd, uid))
        conn.commit()
        cursor.close()
        conn.close()

        # Send Email
        body = f"Hello,\n\nYour temporary password is: {temp_password}\nPlease login and reset your password immediately."
        if send_email(email, "Password Reset", body):
            messagebox.showinfo("Success", f"Temporary password sent to {email}")

    # ================= Face Reset =================
    def reset_via_face(self):
        file_path = filedialog.askopenfilename(title="Select Your Face Image")
        if not file_path:
            return

        unknown_img = face_recognition.load_image_file(file_path)
        unknown_enc = face_recognition.face_encodings(unknown_img)
        if not unknown_enc:
            messagebox.showerror("Error", "No face detected in image")
            return
        unknown_enc = unknown_enc[0]

        known_encodings, known_ids = load_known_faces()
        matched_id = None
        for i, enc in enumerate(known_encodings):
            distance = face_recognition.face_distance([enc], unknown_enc)[0]
            if distance < 0.45:
                matched_id = known_ids[i]
                break

        if not matched_id:
            messagebox.showerror("Error", "Face not recognized")
            return

        # Prompt new password
        self.new_password_popup(matched_id)

    def new_password_popup(self, uid):
        popup = Toplevel(self.root)
        popup.title("Set New Password")
        popup.geometry("400x250")
        popup.resizable(False, False)

        Label(popup, text="New Password", font=("Segoe UI", 12)).pack(pady=10)
        new_pass = Entry(popup, font=("Segoe UI", 12), show="*")
        new_pass.pack(pady=5, fill="x", padx=40)

        Label(popup, text="Confirm Password", font=("Segoe UI", 12)).pack(pady=10)
        confirm_pass = Entry(popup, font=("Segoe UI", 12), show="*")
        confirm_pass.pack(pady=5, fill="x", padx=40)

        def save_password():
            p1 = new_pass.get().strip()
            p2 = confirm_pass.get().strip()
            if not p1 or not p2:
                messagebox.showerror("Error", "Please fill both fields")
                return
            if p1 != p2:
                messagebox.showerror("Error", "Passwords do not match")
                return

            hashed_pwd = hashlib.sha256(p1.encode()).hexdigest()
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE user_registration SET password=%s WHERE unique_id=%s", (hashed_pwd, uid))
            conn.commit()
            cursor.close()
            conn.close()
            messagebox.showinfo("Success", "Password updated successfully")
            popup.destroy()

        Button(popup, text="Save Password", bg="#2563EB", fg="white", font=("Segoe UI", 12, "bold"),
               bd=0, pady=10, command=save_password).pack(pady=20, padx=40, fill="x")

    # ================= Return =================
    def return_to_login(self):
        if self.main_app:
            self.main_app.return_to_main()
        self.destroy()