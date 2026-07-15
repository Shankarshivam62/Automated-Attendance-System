from tkinter import *

class AboutPage(Frame):

    def __init__(self, root, main_app=None):
        super().__init__(root, bg="#F3F4F6")
        self.root = root
        self.main_app = main_app
        self.pack(fill="both", expand=True)

        self.build_ui()

    def build_ui(self):

        # ===== SCROLL SYSTEM =====
        canvas = Canvas(self, bg="#F3F4F6", highlightthickness=0)
        scrollbar = Scrollbar(self, orient="vertical", command=canvas.yview)

        self.scroll_frame = Frame(canvas, bg="#F3F4F6")

        self.scroll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas_window = canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")

        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        canvas.bind("<Configure>", lambda e: canvas.itemconfig(canvas_window, width=e.width))
        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))

        # ===== HEADER =====
        header = Frame(self.scroll_frame, bg="#111827", height=60)
        header.pack(fill="x")

        Button(header, text="← Back",
               bg="#111827", fg="white",
               font=("Segoe UI", 11, "bold"),
               bd=0, cursor="hand2",
               command=self.go_back).pack(side="left", padx=20, pady=10)

        Label(header, text="LogFace - About System",
              bg="#111827", fg="white",
              font=("Segoe UI", 18, "bold")).pack(side="left", padx=10)

        # ===== HERO =====
        hero = Frame(self.scroll_frame, bg="#4F46E5", height=260)
        hero.pack(fill="x")

        Label(hero,
              text="🤖 AI Powered Attendance System",
              bg="#4F46E5", fg="white",
              font=("Segoe UI", 30, "bold")).pack(pady=(60, 10))

        Label(hero,
              text="Smart • Fast • Secure Face Recognition",
              bg="#4F46E5", fg="#E0E7FF",
              font=("Segoe UI", 14)).pack()

        # ===== MAIN CONTENT =====
        container = Frame(self.scroll_frame, bg="#F3F4F6")
        container.pack(pady=30)

        # ===== GRID CARDS =====
        grid = Frame(container, bg="#F3F4F6")
        grid.pack()

        self.card(grid, "📌", "Project Overview",
                  "LogFace is an AI-based system that automates attendance using face recognition technology.\n\n"
                  "It ensures accuracy, saves time, and provides a contactless solution.",
                  0, 0, "#6366F1")

        self.card(grid, "❗", "Problem Solved",
                  "Traditional attendance is slow and prone to errors.\n\n"
                  "This system removes proxy attendance and improves efficiency.",
                  0, 1, "#EF4444")

        self.card(grid, "🧠", "Technology Used",
                  "• Python\n• Tkinter\n• OpenCV\n• Face Recognition\n• Database",
                  1, 0, "#10B981")

        self.card(grid, "🎯", "Objective",
                  "To create a smart system that automates attendance with high accuracy and security.",
                  1, 1, "#F59E0B")

        self.card(grid, "👨‍💻", "Development",
                  "Developed as a B.Tech Computer Science project focusing on AI applications.",
                  2, 0, "#3B82F6")

        self.card(grid, "🚀", "Future Vision",
                  "• Mobile app\n• Cloud system\n• AI improvements\n• Analytics dashboard",
                  2, 1, "#8B5CF6")

        # ===== EXTRA CONTENT =====
        self.section(container, "System Architecture",
                     "📷 Camera → 🧠 Face Detection → 🔍 Recognition → ✅ Attendance → 💾 Database\n\n"
                     "The system captures an image, processes it using AI algorithms, identifies the user, and stores attendance automatically.")

        self.section(container, "Workflow",
                     "1. Capture image from camera\n"
                     "2. Detect face using OpenCV\n"
                     "3. Recognize using trained model\n"
                     "4. Mark attendance\n"
                     "5. Store data in database")

        self.section(container, "Testing & Results",
                     "✔ Accuracy: 95%\n"
                     "✔ Fast response time\n"
                     "✔ Works in real-time environment\n"
                     "✔ Successfully tested with multiple users")

        self.section(container, "Advantages",
                     "• Saves time\n"
                     "• Reduces manual work\n"
                     "• Prevents proxy attendance\n"
                     "• Improves security")

        self.section(container, "Limitations",
                     "• Requires good lighting\n"
                     "• Needs camera setup\n"
                     "• Performance may reduce in low-quality images")

        self.section(container, "Conclusion",
                     "LogFace provides a modern solution for attendance management using AI.\n\n"
                     "It improves efficiency, ensures accuracy, and represents the future of smart systems.")

        # ===== FOOTER =====
        Label(self.scroll_frame,
              text="© 2026 LogFace • AI Attendance System",
              bg="#F3F4F6", fg="#6B7280",
              font=("Segoe UI", 10)).pack(pady=20)

    # ===== CARD =====
    def card(self, parent, icon, title, desc, r, c, color):
        frame = Frame(parent, bg="white", width=260, height=170)
        frame.grid(row=r, column=c, padx=20, pady=20)
        frame.pack_propagate(False)

        circle = Frame(frame, bg=color, width=50, height=50)
        circle.pack(pady=10)
        circle.pack_propagate(False)

        Label(circle, text=icon,
              bg=color, fg="white",
              font=("Segoe UI", 16)).pack(expand=True)

        Label(frame, text=title,
              bg="white", fg="#111827",
              font=("Segoe UI", 12, "bold")).pack()

        Label(frame, text=desc,
              bg="white", fg="#6B7280",
              font=("Segoe UI", 10),
              wraplength=220, justify="center").pack()

        frame.bind("<Enter>", lambda e: frame.config(bg="#EEF2FF"))
        frame.bind("<Leave>", lambda e: frame.config(bg="white"))

    # ===== SECTION TEXT =====
    def section(self, parent, title, content):
        Label(parent, text=title,
              bg="#F3F4F6", fg="#111827",
              font=("Segoe UI", 18, "bold")).pack(anchor="w", pady=10)

        Label(parent, text=content,
              bg="#F3F4F6", fg="#4B5563",
              font=("Segoe UI", 11),
              justify="left", wraplength=900).pack(anchor="w", pady=5)

    # ===== BACK =====
    def go_back(self):
        if self.main_app:
            self.main_app.return_from_about()