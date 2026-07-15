
from tkinter import *
from tkinter import messagebox
import datetime


import os
import cv2
from PIL import Image, ImageTk
import numpy as np
import subprocess
import sys
import db



# ===================== Registration Page =====================
class RegisterPageFrame(Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#EEF2FF")
        self.controller = controller
        self.saved = False
        

        # HEADER
        header = Frame(self, bg="white", height=70)
        header.pack(fill="x")
        Label(header, text="🔷 LogFace", bg="white", fg="#1F2937", font=("Segoe UI", 20, "bold")).pack(side="left", padx=30)
        self.time_label = Label(header, bg="white", fg="#6B7280", font=("Segoe UI", 11))
        self.time_label.pack(side="right", padx=30)
        self.update_time()

        # CENTER CARD
        self.card = Frame(self, bg="white", bd=0)
        self.card.place(relx=0.5, rely=0.55, anchor=CENTER, width=700, height=680)
        Label(self.card, text="Create Your Account", bg="white", fg="#111827", font=("Segoe UI", 24, "bold")).pack(pady=20)
        form_frame = Frame(self.card, bg="white")
        form_frame.pack(pady=10)

        # FORM INPUTS
        self.unique_id = self.create_input(form_frame, "Unique ID *", 0, 0)
        self.first_name = self.create_input(form_frame, "First Name *", 0, 1)
        self.middle_name = self.create_input(form_frame, "Middle Name", 1, 0)
        self.last_name = self.create_input(form_frame, "Last Name *", 1, 1)
        self.email = self.create_input(form_frame, "Email Address *", 2, 0)
        self.phone = self.create_input(form_frame, "Phone Number *", 2, 1)
        self.password = self.create_input(form_frame, "Password *", 3, 0, show="*")
        self.re_password = self.create_input(form_frame, "Re-enter Password *", 3, 1, show="*")

        
        # Show Password
        self.show_var = IntVar()
        Checkbutton(self.card, text="Show Password", variable=self.show_var, bg="white", font=("Segoe UI", 10),
                    command=self.toggle_password).pack(pady=5)

        # Forgot Password
        self.forgot_btn = Button(self.card, text="Forgot Password?", fg="#2563EB", bg="white",
                                 font=("Segoe UI", 10, "underline"), bd=0, cursor="hand2",
                                 command=self.forgot_password)
        self.forgot_btn.pack(pady=(0,5))

        # Error & Saved Labels
        self.error_label = Label(self.card, text="", bg="white", fg="red", font=("Segoe UI", 10))
        self.error_label.pack()
        self.saved_label = Label(self.card, text="", bg="white", fg="#16A34A", font=("Segoe UI", 11), justify=LEFT)
        self.saved_label.pack(pady=(0,5))

        # Buttons
        btn_frame = Frame(self.card, bg="white")
        btn_frame.pack(pady=10)
        self.save_btn = Button(btn_frame, text="✅ Save", bg="#FFFFFF", fg="#111827",
                               font=("Segoe UI", 12, "bold"), width=15, height=2, bd=0,
                               highlightthickness=1, highlightbackground="#B0B0B0", cursor="hand2",
                               command=self.save_registration)
        self.save_btn.pack(side=LEFT, padx=10)

        self.next_btn = Button(
    btn_frame, 
    text="Next ➜", 
    bg="#FFFFFF", fg="#111827",
    font=("Segoe UI", 12, "bold"), width=15, height=2, bd=0,
    highlightthickness=1, highlightbackground="#B0B0B0", cursor="hand2",
    command=self.go_to_face_verification
  # <--- CHANGED
)

        self.next_btn.pack(side=LEFT, padx=10)

        Label(self.card, text="Powered by Automatic Attendance System", bg="white", fg="#6B7280",
              font=("Segoe UI", 9)).pack(side=BOTTOM, pady=10)

    def create_input(self, parent, text, row, column, show=None):
        frame = Frame(parent, bg="white")
        frame.grid(row=row, column=column, padx=20, pady=10)
        Label(frame, text=text, bg="white", fg="#374151", font=("Segoe UI", 10)).pack(anchor="w")
        entry = Entry(frame, font=("Segoe UI", 11), width=30, show=show, relief="flat", bg="#F3F4F6", bd=8)
        entry.pack()
        return entry

    def toggle_password(self):
        if self.show_var.get() == 1:
            self.password.config(show=""); self.re_password.config(show="")
        else:
            self.password.config(show="*"); self.re_password.config(show="*")

    def save_registration(self):
     self.error_label.config(text="", fg="red")

    # Required fields
     if self.unique_id.get() == "" or self.first_name.get() == "" or self.last_name.get() == "" or \
       self.email.get() == "" or self.phone.get() == "" or self.password.get() == "":
        self.error_label.config(text="Please fill all required fields.")
        return

    # Phone validation (10 digits, numbers only)
     if not self.phone.get().isdigit() or len(self.phone.get()) != 10:
        self.error_label.config(text="Phone number must be exactly 10 digits.")
        return

    # Password checks
     if self.password.get() != self.re_password.get():
        self.error_label.config(text="Passwords do not match.")
        return

     if len(self.password.get()) < 6:
        self.error_label.config(text="Password must be at least 6 characters.")
        return
     if db.user_exists(self.unique_id.get()):
       self.error_label.config(text="❌ Unique ID already exists!")
       return

    # (rest of your code continues…)


     db.save_user_to_db(
    self.unique_id.get(),
    self.first_name.get(),
    self.middle_name.get(),
    self.last_name.get(),
    self.email.get(),
    self.phone.get(),
    self.password.get()
   )   
     self.saved_label.config(
            text=f"✅ Saved: {self.unique_id.get()} | {self.first_name.get()} {self.last_name.get()} | {self.email.get()} | {self.phone.get()}",
            fg="#16A34A"
        )
     self.saved = True
    def forgot_password(self):
        popup = Toplevel(self)
        popup.title("Reset Password"); popup.geometry("300x250")
        Label(popup, text="Enter Unique ID:").pack(pady=5); id_entry = Entry(popup); id_entry.pack()
        Label(popup, text="Enter Email:").pack(pady=5); email_entry = Entry(popup); email_entry.pack()
        Label(popup, text="New Password:").pack(pady=5); new_pass = Entry(popup, show="*"); new_pass.pack()
        Label(popup, text="Re-enter New Password:").pack(pady=5); re_pass = Entry(popup, show="*"); re_pass.pack()
        Button(popup, text="Reset Password", bg="#2563EB", fg="white",
               command=lambda: self.reset_password(id_entry.get(), email_entry.get(), new_pass.get(), re_pass.get(), popup)).pack(pady=10)

    def reset_password(self, unique_id, email, new_password, re_password, popup):
        if new_password != re_password:
            messagebox.showerror("Error", "Passwords do not match."); return
        

    def update_time(self):
        now = datetime.datetime.now()
        self.time_label.config(text=now.strftime("%d %B %Y | %I:%M:%S %p"))
        self.after(1000, self.update_time)

    def go_to_face_verification(self):
        if not self.saved:
            messagebox.showwarning("Warning", "Please save your registration first!")
            return
        face_page = self.controller.pages[FaceVerificationFrame]
        face_page.set_user(self.unique_id.get())
        self.controller.show_page(FaceVerificationFrame)
# ===================== Face Verification Page =====================
class FaceVerificationFrame(Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#F4F7FE")
        self.controller = controller
        self.cap = None
        self.running = False
        self.captured_images = 0
        self.required_images = 2
        self.stable_frames = 0
        self.unique_id = None
        # Haar cascades
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        self.eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_eye.xml")
        # Header
        header = Frame(self, bg="white", height=60)
        header.pack(fill="x")
        Label(header, text="🔷 LogFace", bg="white", fg="#111827", font=("Segoe UI", 18, "bold")).pack(side="left", padx=30)
        Label(header, text="Step 2 of 2 • Face Verification", bg="white", fg="#6B7280", font=("Segoe UI", 11)).pack(side="left")

        # Main Card
        self.card = Frame(self, bg="white")
        self.card.place(relx=0.5, rely=0.52, anchor=CENTER, width=1050, height=550)

        self.video_label = Label(self.card, bg="black")
        self.video_label.place(x=40, y=60, width=600, height=420)
        
        Label(self.card, text="AI Face Verification", bg="white", fg="#111827", font=("Segoe UI", 22, "bold")).place(x=700, y=100)
        
        self.status_label = Label(self.card, text="Press Start to begin", bg="white", fg="#DC2626", font=("Segoe UI", 11))
        self.status_label.place(x=700, y=160)
        
        self.progress_label = Label(self.card, text=f"Captured: {self.captured_images} / {self.required_images}", bg="white", fg="#2563EB", font=("Segoe UI", 12, "bold"))
        self.progress_label.place(x=700, y=200)

        # BUTTONS
        self.start_btn = Button(self.card, text="Start Verification", bg="#FFFFFF", fg="#111827", font=("Segoe UI", 12, "bold"), width=22, height=2, bd=0, highlightthickness=1, highlightbackground="#B0B0B0", cursor="hand2", command=self.start_camera)
        self.start_btn.place(x=700, y=260)
        
        self.retake_btn = Button(self.card, text="Retake", bg="#FFFFFF", fg="#111827", font=("Segoe UI", 12, "bold"), width=22, height=2, bd=0, highlightthickness=1, highlightbackground="#B0B0B0", cursor="hand2", command=self.retake)
        self.retake_btn.place(x=700, y=330)

        # FINISH BUTTON (Initially hidden)
          # Inside FaceVerificationFrame in registration.py
        self.finish_btn = Button(
            self.card, 
            text="Finish Registration", 
            bg="#16A34A", 
            fg="white", 
            font=("Segoe UI", 12, "bold"), 
            width=22, 
            height=2, 
            bd=0, 
            cursor="hand2", 
            command=self.finish_and_return
        )

    def set_user(self, unique_id):
     self.unique_id = unique_id

    def finish_and_return(self):
        # Release camera first to prevent memory leaks
        if self.cap:
            self.cap.release()
        
        # Call the main app's return function if it exists
        if self.controller.main_app and hasattr(self.controller.main_app, 'return_to_main'):
            self.controller.main_app.return_to_main()
        else:
            # Fallback if running registration.py standalone
            messagebox.showinfo("Success", "Registration Complete!")
            self.controller.show_page(MainPageFrame)
        
        def update_time(self):
            try:
                if self.winfo_exists():
                    now = datetime.datetime.now()
                    self.time_label.config(text=now.strftime("%d %B %Y | %I:%M:%S %p"))
                    self.after(1000, self.update_time)
            except:
                pass

    def start_camera(self):
        if self.cap is None or not self.cap.isOpened():
            self.cap = cv2.VideoCapture(0)
        
        if not self.cap.isOpened():
            messagebox.showerror("Error", "Camera not detected")
            return
            
        self.running = True
        self.status_label.config(text="Align your face in the frame...", fg="#F59E0B")
        self.update_frame()

    def update_frame(self):
        if not self.running: return
        ret, frame = self.cap.read()
        if not ret: return

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)

        if len(faces) == 0:
            self.stable_frames = 0
            self.status_label.config(text="No face detected.", fg="red")
        elif len(faces) > 1:
            self.stable_frames = 0
            self.status_label.config(text="Multiple faces detected.", fg="red")
        else:
            x, y, w, h = faces[0]
            face_crop = frame[y:y+h, x:x+w]
            eyes = self.eye_cascade.detectMultiScale(cv2.cvtColor(face_crop, cv2.COLOR_BGR2GRAY))
            
            if len(eyes) < 2:
                self.stable_frames = 0
                self.status_label.config(text="Ensure eyes are visible.", fg="red")
            else:
                self.stable_frames += 1
                self.status_label.config(text="Hold steady...", fg="green")
                if self.stable_frames > 20:
                    self.save_face(face_crop)
                    self.stable_frames = 0

            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Display Frame
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame_rgb).resize((600, 420))
        imgtk = ImageTk.PhotoImage(image=img)
        self.video_label.imgtk = imgtk
        self.video_label.configure(image=imgtk)

        if self.captured_images < self.required_images:
            self.after(10, self.update_frame)

    def save_face(self, face_crop):
        if not os.path.exists("faces"):
            os.makedirs("faces")

        filename = f"faces/{self.unique_id}_{self.captured_images+1}.jpg"
        cv2.imwrite(filename, face_crop)

        # ==============================
        # 🔒 DUPLICATE FACE CHECK (IMPORTANT)
        # ==============================
        try:
            import face_recognition
            from db import load_known_faces

            # Encode new face
            rgb_face = cv2.cvtColor(face_crop, cv2.COLOR_BGR2RGB)
            encodings = face_recognition.face_encodings(rgb_face)

            if not encodings:
                messagebox.showerror("Error", "Face not clear. Try again.")
                os.remove(filename)
                return

            new_encoding = encodings[0]

            # Load existing faces
            known_encodings, known_ids = load_known_faces()

            matches = face_recognition.compare_faces(
                known_encodings,
                new_encoding,
                tolerance=0.45
            )

            if True in matches:
                matched_index = matches.index(True)
                matched_id = known_ids[matched_index]

                messagebox.showerror(
                    "Duplicate Face Detected",
                    f"This face is already registered!\nExisting ID: {matched_id}"
                )
                os.remove(filename)
                self.running = False
                if self.cap:
                    self.cap.release()
                return
        except Exception as e:
            messagebox.showerror("Face Check Error", str(e))
            return
        # ✅ SAVE FACE PATH (ONLY IF UNIQUE)
        # ==============================
        try:
            import db
            db.update_face_path(self.unique_id, filename)
        except Exception as e:
            messagebox.showerror("DB Error", str(e))
            return
        self.captured_images += 1
        self.progress_label.config(
            text=f"Captured: {self.captured_images} / {self.required_images}"
        )
        if self.captured_images >= self.required_images:
            self.running = False
            if self.cap:
                self.cap.release()

            self.status_label.config(
                text="Verification Complete ✔",
                fg="#16A34A"
            )
            self.finish_btn.place(x=700, y=400)
    def retake(self):
        self.captured_images = 0
        self.stable_frames = 0
        self.progress_label.config(text=f"Captured: 0 / {self.required_images}")
        self.status_label.config(text="Restarting...", fg="#DC2626")
        self.finish_btn.place_forget() # Hide finish button on retake
        if self.cap: self.cap.release()
        self.start_camera() 
# ===================== Main Page =====================
class MainPageFrame(Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#EEF2FF")
        Label(self, text="Welcome to Main Page!", font=("Segoe UI", 24, "bold"), bg="#EEF2FF").pack(expand=True)
class App(Frame):
    def __init__(self, parent, main_app):
        super().__init__(parent)
        self.main_app = main_app
        self.container = Frame(self, bg="#EEF2FF")
        self.container.pack(fill="both", expand=True)
        self.pages = {}
        for Page in (RegisterPageFrame, FaceVerificationFrame, MainPageFrame):
            page = Page(self.container, self)
            self.pages[Page] = page
            page.place(x=0, y=0, relwidth=1, relheight=1)
        self.show_page(RegisterPageFrame)

    def show_page(self, page_class):
        page = self.pages[page_class]
        page.tkraise()

    def slide_to_page(self, page_class):
        new_page = self.pages[page_class]
        width = self.winfo_width()
        new_page.place(x=width, y=0, relwidth=1, relheight=1)

        def animate():
            x = new_page.winfo_x()
            if x <= 0:
                new_page.place(x=0, y=0)
                return
            new_page.place(x=x - 40, y=0)
            self.after(10, animate)

        animate()
# ===================== RUN =====================
    # Fixed RUN block in registration.py
if __name__ == "__main__":
    root = Tk()
    root.title("Automatic Attendance System")
    root.geometry("1200x750")
    # When running alone, main_app is None
    app = App(root, main_app=None) 
    app.pack(fill="both", expand=True) 
    root.mainloop()