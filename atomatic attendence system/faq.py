from tkinter import *

class FAQPage(Frame):

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

        self.scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
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

        Label(header, text="❓ LogFace FAQ",
              bg="#111827", fg="white",
              font=("Segoe UI", 18, "bold")).pack(side="left", padx=10)

        # ===== HERO =====
        hero = Frame(self.scroll_frame, bg="#6366F1", height=220)
        hero.pack(fill="x")

        Label(hero,
              text="Frequently Asked Questions",
              bg="#6366F1", fg="white",
              font=("Segoe UI", 28, "bold")).pack(pady=(60, 10))

        Label(hero,
              text="Everything you need to know about LogFace",
              bg="#6366F1", fg="#E0E7FF",
              font=("Segoe UI", 12)).pack()

        # ===== CONTAINER =====
        container = Frame(self.scroll_frame, bg="#EEF2FF")
        container.pack(pady=30)

        # ===== FAQ LIST =====
        self.faq_item(container, "🤖 What is LogFace?",
                      "LogFace is an AI-powered attendance system that uses face recognition to automate attendance.\n\n"
                      "It eliminates manual processes and ensures accuracy.")

        self.faq_item(container, "📸 How does face recognition work?",
                      "The system captures an image using a camera, detects the face using OpenCV, and compares it with stored data.\n\n"
                      "If matched, attendance is automatically marked.")

        self.faq_item(container, "⚡ How fast is the system?",
                      "The system works in real-time and can detect and mark attendance within seconds.\n\n"
                      "Performance depends on system hardware and lighting conditions.")

        self.faq_item(container, "📊 What is the accuracy?",
                      "LogFace achieves approximately 95% accuracy under normal lighting conditions.\n\n"
                      "Accuracy may vary depending on camera quality and environment.")

        self.faq_item(container, "🔐 Is the system secure?",
                      "Yes, the system ensures secure authentication and protects user data.\n\n"
                      "Unauthorized users cannot mark attendance.")

        self.faq_item(container, "💻 What technologies are used?",
                      "• Python (Core Language)\n"
                      "• Tkinter (GUI)\n"
                      "• OpenCV (Face Detection)\n"
                      "• AI/ML Algorithms (Recognition)\n"
                      "• Database (Storage)")

        self.faq_item(container, "🏫 Where can this system be used?",
                      "• Schools and Colleges\n"
                      "• Offices and Companies\n"
                      "• Industries\n"
                      "• Any organization requiring attendance tracking")

        self.faq_item(container, "🚀 What are future improvements?",
                      "• Mobile App Integration\n"
                      "• Cloud Database\n"
                      "• Advanced AI Models\n"
                      "• Real-time Analytics Dashboard")

        self.faq_item(container, "❗ What are the limitations?",
                      "• Requires good lighting\n"
                      "• Needs camera setup\n"
                      "• Accuracy may reduce in low-quality images")

        self.faq_item(container, "📈 Why choose LogFace?",
                      "LogFace is fast, secure, and efficient.\n\n"
                      "It reduces manual work and represents the future of smart attendance systems.")

        # ===== FOOTER =====
        Label(self.scroll_frame,
              text="© 2026 LogFace FAQ",
              bg="#EEF2FF", fg="#6B7280",
              font=("Segoe UI", 10)).pack(pady=20)

    # ===== FAQ ITEM =====
    def faq_item(self, parent, question, answer):

        frame = Frame(parent, bg="white", bd=1, relief="solid")
        frame.pack(pady=10, fill="x", padx=30)

        top = Frame(frame, bg="white")
        top.pack(fill="x")

        icon = Label(top, text="❓",
                     bg="#6366F1", fg="white",
                     font=("Segoe UI", 10, "bold"),
                     width=3)
        icon.pack(side="left", padx=10, pady=10)

        lbl = Label(top, text=question,
                    bg="white", fg="#111827",
                    font=("Segoe UI", 12, "bold"))
        lbl.pack(side="left", padx=5)

        toggle = Label(top, text="+",
                       bg="white", fg="#6366F1",
                       font=("Segoe UI", 14, "bold"))
        toggle.pack(side="right", padx=10)

        answer_lbl = Label(frame, text=answer,
                           bg="white", fg="#4B5563",
                           font=("Segoe UI", 11),
                           wraplength=850, justify="left")

        def expand():
            if answer_lbl.winfo_ismapped():
                answer_lbl.pack_forget()
                toggle.config(text="+")
            else:
                answer_lbl.pack(padx=20, pady=10)
                toggle.config(text="−")

        top.bind("<Button-1>", lambda e: expand())
        lbl.bind("<Button-1>", lambda e: expand())
        toggle.bind("<Button-1>", lambda e: expand())

        # Hover
        frame.bind("<Enter>", lambda e: frame.config(bg="#E0E7FF"))
        frame.bind("<Leave>", lambda e: frame.config(bg="white"))

    # ===== BACK =====
    def go_back(self):
        if self.main_app:
            self.main_app.return_from_faq()