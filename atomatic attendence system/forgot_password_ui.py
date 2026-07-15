from tkinter import *
from tkinter import messagebox
import db
import random, string
import smtplib
from email.message import EmailMessage
from reset_password_face import ResetPasswordFace

EMAIL_ADDRESS = "your_email@gmail.com"
EMAIL_PASSWORD = "your_generated_app_password"

def generate_password(length=8):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

def send_email(to_email, subject, body):
    try:
        msg = EmailMessage()
        msg.set_content(body)
        msg["Subject"] = subject
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = to_email

        with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
            smtp.starttls()
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
        return True
    except Exception as e:
        print(str(e))
        return False

class ForgotPasswordApp(Frame):
    def __init__(self, root, main_app=None):
        super().__init__(root, bg="#f5f5f5")
        self.root = root
        self.main_app = main_app
        self.place(relwidth=1, relheight=1)
        self.build_ui()

    def build_ui(self):
        # --- Shadow Frame for Card ---
        shadow = Frame(self, bg="#cbd5e1")
        shadow.place(relx=0.5, rely=0.5, anchor="center", width=520, height=450)

        # --- Main Card ---
        self.card = Frame(self, bg="#ffffff", bd=0, relief="ridge")
        self.card.place(relx=0.5, rely=0.5, anchor="center", width=500, height=430)
        self.card.config(highlightthickness=0)

        # --- Title ---
        Label(self.card, text="🔐 Forgot Password", font=("Segoe UI", 20, "bold"),
              bg="#ffffff", fg="#111827").pack(pady=(20, 5))

        # --- Instruction Panel (slide down) ---
        self.instruction_frame = Frame(self.card, bg="#f0f4f8")
        self.instruction_frame.pack(fill="x", padx=30, pady=(5, 15))
        self.instruction_label = Label(
            self.instruction_frame,
            text="Enter your Unique ID and registered email to reset your password.\n"
                 "Alternatively, use face verification for quick access.",
            font=("Segoe UI", 10), bg="#f0f4f8", fg="#475569",
            justify="center", wraplength=440
        )
        self.instruction_label.pack(pady=10)

        # --- Input Fields ---
        self.create_label_entry("Unique ID")
        self.create_label_entry("Email")

        # --- Feedback / slide message ---
        self.feedback_frame = Frame(self.card, bg="#e0f2fe", height=0)
        self.feedback_frame.pack(fill="x", padx=30, pady=(5,0))
        self.feedback_label = Label(self.feedback_frame, text="", bg="#e0f2fe",
                                    fg="#0369a1", font=("Segoe UI", 10), wraplength=440, justify="center")
        self.feedback_label.pack(pady=5)

        # --- Buttons ---
        btn_frame = Frame(self.card, bg="#ffffff")
        btn_frame.pack(pady=15, fill="x", padx=50)

        self.email_btn = Button(btn_frame, text="Reset via Email", bg="#1e293b", fg="white",
                                font=("Segoe UI", 11, "bold"), bd=0, pady=8, activebackground="#0f172a",
                                command=self.reset_email)
        self.email_btn.pack(fill="x")
        self.email_btn.bind("<Enter>", lambda e: self.email_btn.config(bg="#0f172a"))
        self.email_btn.bind("<Leave>", lambda e: self.email_btn.config(bg="#1e293b"))

        self.face_btn = Button(btn_frame, text="Reset via Face", bg="#475569", fg="white",
                               font=("Segoe UI", 11, "bold"), bd=0, pady=8, activebackground="#1e293b",
                               command=self.reset_face)
        self.face_btn.pack(fill="x", pady=8)
        self.face_btn.bind("<Enter>", lambda e: self.face_btn.config(bg="#1e293b"))
        self.face_btn.bind("<Leave>", lambda e: self.face_btn.config(bg="#475569"))
        # Correct usage inside your button
        # self.face_btn.config(command=lambda: ResetPasswordFace(self.root).start_face_reset(self.card))
        # --- Back to login ---
        self.back_btn = Button(self.card, text="← Back to Login", bg="#f3f4f6", fg="#111827",
                               font=("Segoe UI", 11), bd=0, pady=8, command=self.back_to_login)
        self.back_btn.pack(fill="x", padx=50)

    # --- Utility to create Label + Entry ---
    def create_label_entry(self, text):
        Label(self.card, text=text, bg="#ffffff", fg="#6b7280",
              font=("Segoe UI", 10)).pack(pady=(5, 0))
        entry = Entry(self.card, font=("Segoe UI", 12), bd=1, relief="solid")
        entry.pack(pady=(5, 10), padx=50, fill="x")
        setattr(self, f"{text.lower().replace(' ', '_')}_entry", entry)

    # --- Feedback Slide ---
    def slide_feedback(self, message):
        self.feedback_label.config(text=message)
        height = 0
        def expand():
            nonlocal height
            if height < 40:
                height += 4
                self.feedback_frame.config(height=height)
                self.after(10, expand)
        expand()
        self.after(3000, self.collapse_feedback)

    def collapse_feedback(self):
        height = 40
        def collapse():
            nonlocal height
            if height > 0:
                height -= 4
                self.feedback_frame.config(height=height)
                self.after(10, collapse)
        collapse()

    # --- Reset via Email ---
    def reset_email(self):
        uid = self.unique_id_entry.get().strip()
        email = self.email_entry.get().strip()
        if not uid or not email:
            self.slide_feedback("Please enter both Unique ID and Email.")
            return

        conn = db.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user_registration WHERE unique_id=%s AND email=%s", (uid, email))
        user = cursor.fetchone()
        conn.close()

        if not user:
            self.slide_feedback("Unique ID or Email does not match our records.")
            return

        temp_password = generate_password()
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE user_registration SET password=%s WHERE unique_id=%s", (temp_password, uid))
        conn.commit()
        conn.close()

        body = f"Hello {user['first_name']},\n\nYour temporary password is: {temp_password}\nPlease reset it after login."
        if send_email(email, "LogFace Password Reset", body):
            self.slide_feedback(f"Temporary password sent to {email}")

        from reset_password_face import ResetPasswordFace

    def reset_face(self, card_frame):
        # Pass the card frame to the class
        face_reset = ResetPasswordFace(self.root, card_frame=self.card)
        face_reset.start_face_verification()
    def back_to_login(self):
        self.destroy()
        if self.main_app:
            self.main_app.build_ui()
    

if __name__ == "__main__":
    root = Tk()
    root.geometry("800x600")
    root.title("Forgot Password")
    ForgotPasswordApp(root)
    root.mainloop()