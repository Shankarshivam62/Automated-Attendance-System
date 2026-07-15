from tkinter import *
from tkinter import messagebox
import mysql.connector
import hashlib


# =========================
# DATABASE CONFIG
# =========================
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "Sitaram620@",
    "database": "logface"
}

def get_connection():
    return mysql.connector.connect(**DB_CONFIG)


class LoginApp(Frame):
    def __init__(self, root, main_app=None):
        super().__init__(root)
        self.root = root
        self.main_app = main_app
        self.show_password = False
        self.dark_mode = False
        self.build_ui()

    # ================= UI =================
    def build_ui(self):
        self.configure(bg="#f3f4f6")
        self.place(relwidth=1, relheight=1)

        self.card = Frame(self, bg="white")
        self.card.place(relx=0.5, rely=0.5, anchor="center", width=440, height=520)

        Label(self.card, text="🔐", bg="white", font=("Segoe UI", 40)).pack(pady=(25, 5))
        Label(self.card, text="LogFace Login", bg="white",
              font=("Segoe UI", 22, "bold")).pack(pady=(0, 25))

        # ---------- Unique ID ----------
        self.id_frame = self.create_input("👤", "Unique ID")
        self.id_entry = self.id_frame["entry"]

        # ---------- Password ----------
        self.pass_frame = self.create_input("🔒", "Password", is_password=True)
        self.pass_entry = self.pass_frame["entry"]

        Button(
            self.pass_frame["frame"],
            text="👁",
            bg="white", bd=0, cursor="hand2",
            command=self.toggle_password
        ).pack(side="right", padx=8)

        # ---------- Forgot ----------
        Button(
            self.card, text="Forgot Password?",
            bg="white", fg="#2563EB",
            font=("Segoe UI", 10, "underline"),
            bd=0, cursor="hand2",
            command=self.open_forgot_password_ui  # <-- new method
        ).pack(anchor="e", padx=40, pady=(0, 15))
        
        # ---------- Login Button ----------
        self.login_btn = Button(
            self.card, text="🔐 Login",
            bg="#2563EB", fg="white",
            font=("Segoe UI", 12, "bold"),
            bd=0, pady=12,
            cursor="hand2",
            command=self.login_user
        )
        self.login_btn.pack(padx=40, fill="x")

        # ---------- Loader ----------
        self.loader = Label(
            self.card, text="", bg="white",
            font=("Segoe UI", 10)
        )
        self.loader.pack(pady=8)

        # ---------- Face Login ----------
        Button(
            self.card, text="👤 Login with Face",
            bg="#10B981", fg="white",
            font=("Segoe UI", 11, "bold"),
            bd=0, pady=10,
            cursor="hand2",
            command=self.face_login
        ).pack(padx=40, pady=(5, 10), fill="x")

        # ---------- Dark Mode ----------
        Button(
            self.card, text="🌙 Toggle Dark Mode",
            bg="#E5E7EB", bd=0,
            cursor="hand2",
            command=self.toggle_dark_mode
        ).pack(padx=40, fill="x")

        Button(
            self.card, text="← Back",
            bg="#F3F4F6", bd=0,
            command=self.return_to_main
        ).pack(padx=40, pady=10, fill="x")

        Label(
            self.card, text="© 2026 LogFace Inc.",
            bg="white", fg="#9CA3AF",
            font=("Segoe UI", 9)
        ).pack(side="bottom", pady=12)

    # ================= INPUT CREATOR =================
    def create_input(self, icon, placeholder, is_password=False):
        frame = Frame(self.card, bg="white", width=320, height=44,
                      highlightthickness=1, highlightbackground="#D1D5DB")
        frame.pack(padx=40, pady=(0, 15))
        frame.pack_propagate(False)

        Label(frame, text=icon, bg="white", font=("Segoe UI", 14)).pack(side="left", padx=8)

        entry = Entry(frame, bd=0, font=("Segoe UI", 12), fg="#6B7280")
        entry.pack(side="left", fill="both", expand=True)
        entry.insert(0, placeholder)

        entry.bind("<FocusIn>", lambda e: self.clear_placeholder(entry, placeholder, is_password))
        entry.bind("<FocusOut>", lambda e: self.add_placeholder(entry, placeholder))

        return {"frame": frame, "entry": entry}

    # ================= HELPERS =================
    def clear_placeholder(self, entry, text, is_password=False):
        if entry.get() == text:
            entry.delete(0, END)
            entry.config(fg="#111827")
            if is_password:
                entry.config(show="*" if not self.show_password else "")

    def add_placeholder(self, entry, text):
        if not entry.get():
            entry.insert(0, text)
            entry.config(fg="#6B7280", show="")

    def toggle_password(self):
        self.show_password = not self.show_password
        if self.pass_entry.get() != "Password":
            self.pass_entry.config(show="" if self.show_password else "*")

    def mark_error(self, entry):
        entry.master.config(highlightbackground="red", highlightthickness=2)

    def reset_error(self, entry):
        entry.master.config(highlightbackground="#D1D5DB", highlightthickness=1)

    # ================= PASSWORD HASH =================
    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    # ================= LOGIN =================
    def login_user(self):
        uid = self.id_entry.get().strip()
        pwd = self.pass_entry.get().strip()

        # Reset errors
        self.reset_error(self.id_entry)
        self.reset_error(self.pass_entry)

        # Validation
        if uid in ("", "Unique ID"):
            self.mark_error(self.id_entry)
            self.id_entry.focus()
            return

        if pwd in ("", "Password"):
            self.mark_error(self.pass_entry)
            self.pass_entry.focus()
            return

        # UI feedback
        self.login_btn.config(state=DISABLED, text="Logging in...")
        self.loader.config(text="Please wait...")

        # Delay to show loader, then login
        self.after(500, lambda: self._do_login(uid, pwd))
        
    def _do_login(self, uid, pwd):
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                "SELECT * FROM user_registration WHERE unique_id=%s AND password=%s",
                (uid, pwd)
            )
            user = cursor.fetchone()
            conn.close()

            # Restore button
            self.login_btn.config(state=NORMAL, text="🔐 Login")
            self.loader.config(text="")

            if user:
            #    messagebox.showinfo("Success", f"Welcome {user['first_name']}")
                if self.main_app:
                 self.main_app.logged_user = user
 
            # self.destroy()
            # Open main page
            
            #  if self.main_app:
                self.main_app.build_ui()
                self.return_to_main()
            else:
                self.mark_error(self.id_entry)
                self.mark_error(self.pass_entry)
                messagebox.showerror("Login Failed", "Invalid Unique ID or Password")

        except Exception as e:
            self.login_btn.config(state=NORMAL, text="🔐 Login")
            self.loader.config(text="")
            messagebox.showerror("Database Error", str(e))   
        
    # ================= FACE LOGIN =================
    def face_login(self):
        from face_login_ui import FaceLoginApp
        FaceLoginApp(self.root, main_app=self.main_app)
     # ================= DARK MODE =================
    def toggle_dark_mode(self):
        self.dark_mode = not self.dark_mode
        bg = "#111827" if self.dark_mode else "#f3f4f6"
        card = "#1F2933" if self.dark_mode else "white"
        fg = "white" if self.dark_mode else "#111827"

        self.config(bg=bg)
        self.card.config(bg=card)

        for widget in self.card.winfo_children():
            try:
                widget.config(bg=card, fg=fg)
            except:
                pass

    def forgot_password(self):
        messagebox.showinfo("Forgot Password", "Contact admin to reset password.")

    def return_to_main(self):
        if self.main_app:
            self.main_app.return_to_main()
            
    def open_forgot_password_ui(self):
        from forgot_password_ui import ForgotPasswordApp

        width = self.root.winfo_width()
        forgot_frame = ForgotPasswordApp(self.root)
        forgot_frame.place(x=width, y=0, relwidth=1, relheight=1)

        # Slide animation
        def slide():
            x = forgot_frame.winfo_x()
            if x <= 0:
                forgot_frame.place(x=0, y=0)
                return
            forgot_frame.place(x=x - 40, y=0)
            self.root.after(10, slide)
        slide()        