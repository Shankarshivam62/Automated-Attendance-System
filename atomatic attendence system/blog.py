from tkinter import *

class BlogPage(Frame):

    def __init__(self, root, main_app=None):
        super().__init__(root, bg="#EEF2FF")
        self.root = root
        self.main_app = main_app
        self.pack(fill="both", expand=True)

        self.build_ui()

    def build_ui(self):

        # ===== SCROLL =====
        canvas = Canvas(self, bg="#EEF2FF", highlightthickness=0)
        scrollbar = Scrollbar(self, orient="vertical", command=canvas.yview)

        self.scroll_frame = Frame(canvas, bg="#EEF2FF")

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

        Label(header, text="📰 LogFace Blog",
              bg="#111827", fg="white",
              font=("Segoe UI", 18, "bold")).pack(side="left", padx=10)

        # ===== HERO =====
        hero = Frame(self.scroll_frame, bg="#4F46E5", height=230)
        hero.pack(fill="x")

        Label(hero,
              text="✨ Insights & Innovations",
              bg="#4F46E5", fg="white",
              font=("Segoe UI", 28, "bold")).pack(pady=(60, 10))

        Label(hero,
              text="AI • Security • Smart Systems",
              bg="#4F46E5", fg="#E0E7FF",
              font=("Segoe UI", 12)).pack()

        # ===== BLOG AREA =====
        container = Frame(self.scroll_frame, bg="#EEF2FF")
        container.pack(pady=30)

        # BLOG POSTS
        self.blog_card(container, "🤖", "Face Recognition Technology",
                       "AI",
                       "Face recognition identifies users using facial features.\nUsed in security, mobile unlock, and smart attendance systems.",
                       "#6366F1")

        self.blog_card(container, "📊", "Why Smart Attendance Matters",
                       "System",
                       "Automated attendance reduces errors, saves time, and prevents proxy attendance.",
                       "#10B981")

        self.blog_card(container, "🧠", "How LogFace Works",
                       "Technology",
                       "Camera captures face → AI detects → System recognizes → Attendance marked automatically.",
                       "#F59E0B")

        self.blog_card(container, "🔐", "Security in AI Systems",
                       "Security",
                       "Data protection and secure authentication are essential in face recognition systems.",
                       "#EF4444")

        self.blog_card(container, "🚀", "Future of Smart Systems",
                       "Future",
                       "AI systems will evolve with cloud integration, mobile apps, and real-time analytics.",
                       "#8B5CF6")

        # ===== FOOTER =====
        Label(self.scroll_frame,
              text="© 2026 LogFace Blog",
              bg="#EEF2FF", fg="#6B7280",
              font=("Segoe UI", 10)).pack(pady=20)

    # ===== BLOG CARD =====
    def blog_card(self, parent, icon, title, tag, content, color):

        frame = Frame(parent, bg="white", width=900, height=180)
        frame.pack(pady=15)
        frame.pack_propagate(False)

        top = Frame(frame, bg="white")
        top.pack(fill="x", pady=10)

        # ICON CIRCLE
        circle = Frame(top, bg=color, width=45, height=45)
        circle.pack(side="left", padx=15)
        circle.pack_propagate(False)

        Label(circle, text=icon,
              bg=color, fg="white",
              font=("Segoe UI", 14)).pack(expand=True)

        # TITLE + TAG
        text_frame = Frame(top, bg="white")
        text_frame.pack(side="left")

        Label(text_frame, text=title,
              bg="white", fg="#111827",
              font=("Segoe UI", 13, "bold")).pack(anchor="w")

        Label(text_frame, text=tag,
              bg="#E0E7FF", fg="#4338CA",
              font=("Segoe UI", 9, "bold"),
              padx=8, pady=2).pack(anchor="w", pady=3)

        # CONTENT
        Label(frame, text=content,
              bg="white", fg="#4B5563",
              font=("Segoe UI", 11),
              wraplength=820, justify="left").pack(anchor="w", padx=20)

        # Hover effect
        frame.bind("<Enter>", lambda e: frame.config(bg="#E0E7FF"))
        frame.bind("<Leave>", lambda e: frame.config(bg="white"))

    # ===== BACK =====
    def go_back(self):
        if self.main_app:
            self.main_app.return_from_blog()