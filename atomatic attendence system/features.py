from tkinter import *

class FeaturesPage(Frame):

    def __init__(self, root, main_app=None):
        super().__init__(root, bg="white")
        self.root = root
        self.main_app = main_app
        self.build_ui()

    def build_ui(self):

        # ===== SCROLLABLE CANVAS =====
        self.canvas = Canvas(self, bg="white", highlightthickness=0)
        scrollbar = Scrollbar(self, orient="vertical", command=self.canvas.yview)

        self.scroll_frame = Frame(self.canvas, bg="white")

        self.scroll_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas_window = self.canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # FULL WIDTH FIX
        self.canvas.bind("<Configure>", lambda e: self.canvas.itemconfig(self.canvas_window, width=e.width))

        # SMOOTH SCROLL
        self.canvas.bind("<Enter>", lambda e: self.canvas.bind_all("<MouseWheel>", self._on_scroll))
        self.canvas.bind("<Leave>", lambda e: self.canvas.unbind_all("<MouseWheel>"))

        # ===== NAVBAR =====
        navbar = Frame(self.scroll_frame, bg="white", height=60)
        navbar.pack(fill="x")

        Label(navbar, text="🔷 LogFace",
              bg="white", fg="#111827",
              font=("Segoe UI", 18, "bold")).pack(side="left", padx=20)

        Button(navbar, text="← Back",
               bg="white", fg="#2563EB",
               font=("Segoe UI", 11, "bold"),
               bd=0, cursor="hand2",
               command=self.go_back).pack(side="right", padx=20)

        # ===== HERO =====
        hero = Frame(self.scroll_frame, bg="#4F46E5", height=320)
        hero.pack(fill="x")

        Label(hero, text="AI Powered Attendance System",
              bg="#4F46E5", fg="white",
              font=("Segoe UI", 30, "bold")).pack(pady=(80, 10))

        Label(hero, text="Smart • Fast • Secure Face Recognition",
              bg="#4F46E5", fg="#E0E7FF",
              font=("Segoe UI", 14)).pack()

        Button(hero, text="🚀 Get Started",
               bg="white", fg="#4F46E5",
               font=("Segoe UI", 12, "bold"),
               padx=20, pady=8,
               bd=0).pack(pady=20)

        # ===== INTRO =====
        Label(self.scroll_frame,
              text="Why Choose LogFace?",
              bg="white", fg="#111827",
              font=("Segoe UI", 24, "bold")).pack(pady=30)

        Label(self.scroll_frame,
              text="LogFace is an advanced AI-powered attendance management system designed to automate and simplify the traditional attendance process. ",
              bg="white", fg="#6B7280",
              font=("Segoe UI", 12),
              wraplength=900, justify="center").pack(pady=10)

        # ===== FEATURES =====
        container = Frame(self.scroll_frame, bg="white")
        container.pack(pady=20)

        features = [
            ("🎯", "Face Recognition", "Detect faces automatically"),
            ("📊", "Analytics Dashboard", "Track attendance insights"),
            ("📁", "Export Reports", "Download CSV reports"),
            ("🔐", "Secure System", "Protected login system"),
            ("🎥", "Live Detection", "Real-time camera tracking"),
            ("🌙", "Dark Mode", "Switch themes easily"),
            ("⚡", "Fast Processing", "Optimized performance"),
            ("📱", "Modern UI", "Clean user interface"),
        ]

        for i, (icon, title, desc) in enumerate(features):
            card = Frame(container, bg="#F9FAFB", width=260, height=160, bd=1, relief="solid")
            card.grid(row=i//4, column=i%4, padx=20, pady=20)
            card.pack_propagate(False)

            card.bind("<Enter>", lambda e, c=card: c.config(bg="#EEF2FF"))
            card.bind("<Leave>", lambda e, c=card: c.config(bg="#F9FAFB"))

            Label(card, text=icon, font=("Segoe UI", 30), bg=card["bg"]).pack(pady=10)
            Label(card, text=title, font=("Segoe UI", 12, "bold"), bg=card["bg"]).pack()
            Label(card, text=desc, font=("Segoe UI", 10),
                  bg=card["bg"], fg="#6B7280",
                  wraplength=200).pack()

        # ===== HOW IT WORKS =====
        Label(self.scroll_frame,
      text="System Overview",
      bg="white", fg="#111827",
      font=("Segoe UI", 22, "bold")).pack(pady=30)

        Label(self.scroll_frame,
            text="The LogFace system integrates computer vision and machine learning technologies to provide a seamless attendance experience. It captures facial features, processes them using trained models, and verifies identity instantly.\n\nThe system is designed to handle multiple users efficiently and can be integrated with databases for long-term storage and analytics. Its modular design allows future scalability and enhancements.",
            bg="white", fg="#4B5563",
            font=("Segoe UI", 12),
            wraplength=900, justify="center").pack(pady=10)

        steps = [
            "📸 Capture face using camera",
            "🧠 AI processes and identifies user",
            "✅ Attendance marked automatically",
            "📊 Data stored and analyzed"
        ]

        for step in steps:
            Label(self.scroll_frame, text=step,
                  bg="white", fg="#374151",
                  font=("Segoe UI", 12)).pack(pady=5)

        # ===== PERFORMANCE =====
        Label(self.scroll_frame, text="System Performance",
              bg="white", font=("Segoe UI", 22, "bold")).pack(pady=30)

        self.create_bar( "Face Recognition Accuracy",  95,
            "The system achieves high accuracy using advanced machine learning algorithms that can detect and recognize faces even under different lighting and angles."
        )
        self.create_bar( "Processing Speed", 90,
            "Optimized algorithms ensure fast detection and recognition, allowing real-time attendance marking without delay."
        )
        self.create_bar(  "System Security", 92,
            "User data is securely stored and protected with authentication mechanisms, preventing unauthorized access and ensuring privacy."
        )
        
        # ===== USE CASES =====
        Label(self.scroll_frame, text="Where It Is Used",
              bg="white", font=("Segoe UI", 22, "bold")).pack(pady=30)

        for t in ["🏫 Schools", "🏢 Offices", "🏭 Industries", "🏥 Hospitals"]:
            Label(self.scroll_frame, text=t, bg="white", font=("Segoe UI", 12)).pack(pady=5)

        # ===== TECHNOLOGY =====
        Label(self.scroll_frame, text="Technology Used",
              bg="white", font=("Segoe UI", 22, "bold")).pack(pady=30)

        for t in ["Python", "OpenCV", "Machine Learning", "Database", "Tkinter"]:
            Label(self.scroll_frame, text=t, bg="white", font=("Segoe UI", 12)).pack(pady=5)

        # ===== ADVANTAGES =====
        Label(self.scroll_frame, text="Advantages",
              bg="white", font=("Segoe UI", 22, "bold")).pack(pady=30)

        for a in ["✔ Saves Time", "✔ Accurate", "✔ Automated", "✔ Secure"]:
            Label(self.scroll_frame, text=a, fg="green",
                  bg="white", font=("Segoe UI", 12)).pack(pady=5)

        # ===== FUTURE =====
        Label(self.scroll_frame, text="Future Scope",
              bg="white", font=("Segoe UI", 22, "bold")).pack(pady=30)

        for f in ["Mobile App", "Cloud Storage", "Advanced Analytics"]:
            Label(self.scroll_frame, text=f, bg="white",
                  font=("Segoe UI", 12)).pack(pady=5)

        # ===== CTA =====
        cta = Frame(self.scroll_frame, bg="#111827", height=200)
        cta.pack(fill="x", pady=40)

        Label(cta, text="Start Using Smart Attendance Today",
              bg="#111827", fg="white",
              font=("Segoe UI", 20, "bold")).pack(pady=60)

        # ===== FOOTER =====
        Label(self.scroll_frame,
              text="© 2026 LogFace",
              bg="white", fg="#6B7280").pack(pady=20)

    def create_bar(self, title, value, description):
        frame = Frame(self.scroll_frame, bg="white")
        frame.pack(fill="x", padx=150, pady=12)

        # Title + Percentage
        top = Frame(frame, bg="white")
        top.pack(fill="x")

        Label(top, text=title,
            bg="white", fg="#111827",
            font=("Segoe UI", 12, "bold")).pack(side="left")

        Label(top, text=f"{value}%",
            bg="white", fg="#4F46E5",
            font=("Segoe UI", 11, "bold")).pack(side="right")

        # Progress bar
        bar_bg = Frame(frame, bg="#E5E7EB", height=12)
        bar_bg.pack(fill="x", pady=5)

        bar = Frame(bar_bg, bg="#4F46E5", width=value*5, height=12)
        bar.pack(side="left")

        # Description
        Label(frame, text=description,
            bg="white", fg="#6B7280",
            font=("Segoe UI", 10),
            wraplength=800, justify="left").pack(anchor="w")
        frame = Frame(self.scroll_frame, bg="white")
        frame.pack(fill="x", padx=150, pady=5)

        
        bar_bg = Frame(frame, bg="#E5E7EB", height=10)
        bar_bg.pack(fill="x")

        bar = Frame(bar_bg, bg="#4F46E5", width=value*4, height=10)
        bar.pack(side="left")

    def _on_scroll(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def go_back(self):
        if self.main_app:
            self.main_app.return_from_features()