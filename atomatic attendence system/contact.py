from tkinter import *
import webbrowser
import smtplib
from email.mime.text import MIMEText
from tkinter import messagebox
class ContactPage(Frame):

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

        Label(header, text="📞 Contact Us",
              bg="#111827", fg="white",
              font=("Segoe UI", 18, "bold")).pack(side="left", padx=10)

        # ===== HERO =====
        hero = Frame(self.scroll_frame, bg="#4F46E5", height=220)
        hero.pack(fill="x")

        Label(hero,
              text="Get in Touch",
              bg="#4F46E5", fg="white",
              font=("Segoe UI", 28, "bold")).pack(pady=(60, 10))

        Label(hero,
              text="We'd love to hear from you 🚀",
              bg="#4F46E5", fg="#E0E7FF",
              font=("Segoe UI", 12)).pack()

        # ===== CONTACT CARDS =====
        cards = Frame(self.scroll_frame, bg="#EEF2FF")
        cards.pack(pady=30)

        self.contact_card(cards, "📞 Phone", "+91 9905657629",
                          lambda: webbrowser.open("tel:+919905657629"), "#10B981")

        self.contact_card(cards, "💬 WhatsApp", "Chat on WhatsApp",
                          lambda: webbrowser.open("https://wa.me/919905657629"), "#25D366")

        self.contact_card(cards, "📸 Instagram", "@logface_ai",
                          lambda: webbrowser.open("https://www.instagram.com/shivam_yadav.00?igsh=Z290NW1oNTRvcGZ6"), "#E1306C")

        self.contact_card(cards, "✉ Email", "Shivamshankar266@gmail.com",
                            lambda: webbrowser.open("https://mail.google.com/mail/?view=cm&fs=1&to=ShivamShankar266@gmail.com"),
                            "#3B82F6")
        # ===== FORM =====
        form = Frame(self.scroll_frame, bg="white")
        form.pack(pady=30, padx=40, fill="x")

        Label(form, text="Send Message",
              bg="white", fg="#111827",
              font=("Segoe UI", 18, "bold")).pack(pady=10)

        Label(form, text="Your Name").pack(anchor="w", padx=10)
        self.name_entry = Entry(form)
        self.name_entry.pack(fill="x", padx=10, pady=5)
        Label(form, text="Your Email").pack(anchor="w", padx=10)
        self.email_entry = Entry(form)
        self.email_entry.pack(fill="x", padx=10, pady=5)
        
        Label(form, text="Message",
              bg="white", fg="#374151",
              font=("Segoe UI", 11)).pack(anchor="w", padx=10)

        self.msg = Text(form, height=4)
        self.msg.pack(fill="x", padx=10, pady=5)

        Button(form, text="Send Message",
               bg="#4F46E5", fg="white",
               font=("Segoe UI", 12, "bold"),
               bd=0, pady=8, cursor="hand2",
               command=self.send_msg).pack(pady=15)

        # ===== FOOTER =====
        Label(self.scroll_frame,
              text="© 2026 LogFace Contact",
              bg="#EEF2FF", fg="#6B7280",
              font=("Segoe UI", 10)).pack(pady=20)

    # ===== CONTACT CARD =====
    def contact_card(self, parent, title, subtitle, command, color):

        frame = Frame(parent, bg="white", width=850, height=80)
        frame.pack(pady=10)
        frame.pack_propagate(False)

        left = Frame(frame, bg=color, width=60)
        left.pack(side="left", fill="y")

        Label(left, text=title[0],
              bg=color, fg="white",
              font=("Segoe UI", 18, "bold")).pack(expand=True)

        text = Frame(frame, bg="white")
        text.pack(side="left", padx=15)

        Label(text, text=title,
              bg="white", fg="#111827",
              font=("Segoe UI", 12, "bold")).pack(anchor="w")

        Label(text, text=subtitle,
              bg="white", fg="#6B7280",
              font=("Segoe UI", 10)).pack(anchor="w")

        Button(frame, text="Open",
               bg="#4F46E5", fg="white",
               bd=0, padx=10, cursor="hand2",
               command=command).pack(side="right", padx=15)

        frame.bind("<Enter>", lambda e: frame.config(bg="#E0E7FF"))
        frame.bind("<Leave>", lambda e: frame.config(bg="white"))

    # ===== ENTRY =====
    def entry(self, parent, label):
        Label(parent, text=label,
              bg="white", fg="#374151",
              font=("Segoe UI", 11)).pack(anchor="w", padx=10)

        e = Entry(parent)
        e.pack(fill="x", padx=10, pady=5)

    # ===== SEND =====
 
    from email.mime.text import MIMEText

    # ===== SEND =====
    def send_msg(self):

            name = self.name_entry.get()
            email = self.email_entry.get()
            message = self.msg.get("1.0", END)

            sender_email = "Shivamshankar266@gmail.com"
            app_password = "rdjurrltdahmkgqu"   # ⚠ remove spaces
            receiver_email = "shivamshankar266@gmail.com"

            subject = "New Contact Message from LogFace"

            body = f"""
    Name: {name}
    Email: {email}

    Message:
    {message}
    """

            msg = MIMEText(body)
            msg["Subject"] = subject
            msg["From"] = sender_email
            msg["To"] = receiver_email

            try:
                server = smtplib.SMTP("smtp.gmail.com", 587)
                server.starttls()
                server.login(sender_email, app_password)
                server.send_message(msg)
                server.quit()

                messagebox.showinfo("Success", "Message sent successfully ✅")

            except Exception as e:
                messagebox.showerror("Error", f"Failed ❌\n{e}")

        # ===== BACK =====
    def go_back(self):
            if self.main_app:
                self.main_app.return_from_contact()
        