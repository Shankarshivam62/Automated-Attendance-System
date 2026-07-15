from tkinter import *
from tkinter import ttk
from tkinter import messagebox

class HelpPage(Frame):
    def __init__(self, root, main_app=None):
        super().__init__(root, bg="#F3F4F6")
        self.root = root
        self.main_app = main_app
        self.build_ui()

    def build_ui(self):
        # ===== HEADER =====
        header = Frame(self, bg="#4F46E5", height=90)
        header.pack(fill="x")
        Button(header, text="← Back", bg="#2563EB", fg="white",
               font=("Segoe UI", 14, "bold"), bd=0, cursor="hand2",
               command=self.return_to_main).pack(side=LEFT, padx=20, pady=20)
        Label(header, text="💡 LogFace Help Center", bg="#4F46E5", fg="white",
              font=("Segoe UI", 24, "bold")).pack(side=LEFT, padx=20, pady=20)

        # ===== SCROLLABLE CANVAS =====
        canvas = Canvas(self, bg="#F3F4F6", highlightthickness=0)
        canvas.pack(side=LEFT, fill=BOTH, expand=True)

        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        canvas.configure(yscrollcommand=scrollbar.set)

        self.content_frame = Frame(canvas, bg="#F3F4F6")
        canvas.create_window((0, 0), window=self.content_frame, anchor="nw")

        # ===== HELP TOPICS DATA =====
        self.topics = [
            {"icon": "📝", "title": "Registration", "steps": [
                ("1️⃣", "Click 'Register' in the top navbar."),
                ("2️⃣", "Fill your personal details (name, email, password)."),
                ("3️⃣", "Click 'Submit' to create your account."),
                ("4️⃣", "You will get a confirmation message.")
            ]},
            {"icon": "🔑", "title": "Login", "steps": [
                ("1️⃣", "Click 'Login' in the navbar."),
                ("2️⃣", "Enter your registered email and password."),
                ("3️⃣", "Click 'Login' to access the dashboard."),
                ("4️⃣", "If login fails, check your credentials.")
            ]},
            {"icon": "✅", "title": "Mark Attendance", "steps": [
                ("1️⃣", "Go to the side menu and click 'Mark Attendance'."),
                ("2️⃣", "Allow camera access."),
                ("3️⃣", "Look at the camera for face recognition."),
                ("4️⃣", "Attendance will be automatically marked.")
            ]},
            {"icon": "📊", "title": "Attendance History", "steps": [
                ("1️⃣", "Click 'Attendance History' in the side menu."),
                ("2️⃣", "View your daily, weekly, or monthly attendance."),
                ("3️⃣", "Export the attendance as CSV if needed.")
            ]},
            {"icon": "🎥", "title": "Camera Settings", "steps": [
                ("1️⃣", "Click 'Camera Settings' in the side menu."),
                ("2️⃣", "Adjust brightness, contrast, and camera angle."),
                ("3️⃣", "Save settings to improve recognition accuracy.")
            ]},
        ]

        # ===== CREATE TOPIC CARDS WITH GRADIENT & ICONS =====
        for topic in self.topics:
            self.create_gradient_card(topic)

        # ===== CHATBOT PANEL =====
        self.chat_frame = Frame(self, bg="#E5E7EB", width=320)
        self.chat_frame.pack(side=RIGHT, fill=Y)
        Label(self.chat_frame, text="🤖 Chatbot Assistant", bg="#E5E7EB",
              font=("Segoe UI", 14, "bold")).pack(pady=10)

        self.chat_text = Text(self.chat_frame, height=25, width=40, state=DISABLED, bg="white")
        self.chat_text.pack(padx=10, pady=5)

        self.chat_entry = Entry(self.chat_frame, font=("Segoe UI", 12))
        self.chat_entry.pack(padx=10, pady=5, fill=X)
        self.chat_entry.bind("<Return>", self.send_chat)

        Button(self.chat_frame, text="Send", bg="#2563EB", fg="white",
               font=("Segoe UI", 12, "bold"), bd=0, cursor="hand2",
               command=self.send_chat).pack(pady=5)

    def create_gradient_card(self, topic):
        # Outer card with shadow effect
        card_border = Frame(self.content_frame, bg="#CBD5E1", bd=0)
        card_border.pack(padx=20, pady=10, fill="x")
        card = Frame(card_border, bg="#FFFFFF", bd=0, relief="flat")
        card.pack(padx=2, pady=2, fill="x")

        # Top: Icon + Title
        top_frame = Frame(card, bg="#FFFFFF")
        top_frame.pack(fill="x", pady=5, padx=5)
        Label(top_frame, text=topic["icon"], font=("Segoe UI", 28), bg="#FFFFFF").pack(side=LEFT, padx=10)
        Label(top_frame, text=topic["title"], font=("Segoe UI", 16, "bold"), bg="#FFFFFF").pack(side=LEFT, padx=10)

        toggle_btn = Button(top_frame, text="▼", bg="#FFFFFF", bd=0, cursor="hand2",
                            font=("Segoe UI", 12, "bold"))
        toggle_btn.pack(side=RIGHT, padx=10)

        # Content Frame
        content_frame = Frame(card, bg="#F1F5F9")
        content_frame.pack(fill="x", padx=10, pady=5)
        content_frame.visible = False
        content_frame.for_toggle_btn = toggle_btn

        # Add steps with icons
        for icon, step in topic["steps"]:
            Label(content_frame, text=f"{icon} {step}", font=("Segoe UI", 13),
                  bg="#F1F5F9", anchor="w", justify=LEFT, wraplength=600).pack(fill="x", padx=15, pady=2)

        content_frame.pack_forget()

        toggle_btn.config(command=lambda: self.toggle_accordion(content_frame))

    def toggle_accordion(self, frame):
        if frame.visible:
            self.slide_up(frame)
            frame.visible = False
            frame.for_toggle_btn.config(text="▼")
        else:
            frame.pack(fill="x", padx=10, pady=5)
            self.slide_down(frame)
            frame.visible = True
            frame.for_toggle_btn.config(text="▲")

    def slide_down(self, frame, h=0):
        if h < frame.winfo_reqheight():
            h += 10
            frame.config(height=h)
            self.after(10, lambda: self.slide_down(frame, h))
        else:
            frame.config(height='')

    def slide_up(self, frame, h=None):
        if h is None:
            h = frame.winfo_height()
        if h > 0:
            h -= 10
            frame.config(height=h)
            self.after(10, lambda: self.slide_up(frame, h))
        else:
            frame.pack_forget()
            frame.config(height='')

    # ===== SIMPLE AI-STYLE CHATBOT =====
    def send_chat(self, event=None):
        question = self.chat_entry.get().strip()
        if not question:
            return
        self.chat_entry.delete(0, END)

        self.chat_text.config(state=NORMAL)
        self.chat_text.insert(END, f"You: {question}\n")
        self.chat_text.config(state=DISABLED)
        self.chat_text.see(END)

        # Rule-based AI response (replaceable with real AI later)
        question_lower = question.lower()
        response = "🤖 Sorry, I cannot answer that. Try keywords like 'register', 'login', 'attendance'."
        if "register" in question_lower:
            response = "🤖 To register, click 'Register' and fill in your details."
        elif "login" in question_lower:
            response = "🤖 To login, click 'Login' and enter your email & password."
        elif "attendance" in question_lower:
            response = "🤖 Mark attendance from the side menu → 'Mark Attendance'."
        elif "history" in question_lower:
            response = "🤖 View your attendance history from 'Attendance History'."

        self.chat_text.config(state=NORMAL)
        self.chat_text.insert(END, f"{response}\n\n")
        self.chat_text.config(state=DISABLED)
        self.chat_text.see(END)

    def return_to_main(self):
        if self.main_app:
            self.main_app.return_from_help()