from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import db
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from EditProfilePage import EditProfilePage

class ProfilePage(Frame):
    def __init__(self, root, user, main_app):
        super().__init__(root, bg="#0F172A")  # Dark background
        self.root = root
        self.user = user
        self.main_app = main_app

        self.place(x=0, y=0, relwidth=1, relheight=1)
        self.build_ui()
    def show_graph(self, parent):
        dates = db.get_attendance_by_date(self.user.get("unique_id"))

        if not dates:
            Label(parent, text="No attendance data",
                bg="#111827", fg="white").pack()
            return

        # Convert dates into counts
        date_counts = {}
        for d in dates:
            date_counts[d] = date_counts.get(d, 0) + 1

        x = list(date_counts.keys())
        y = list(date_counts.values())

        # Create figure
        fig = plt.Figure(figsize=(5, 3), dpi=100)
        ax = fig.add_subplot(111)
        ax.plot(x, y, marker='o')
        ax.set_title("Attendance Graph")
        ax.set_xlabel("Date")
        ax.set_ylabel("Marks")

        # Embed in Tkinter
        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def build_ui(self):
        stats = db.get_attendance_stats(self.user.get("unique_id"))
        # ===== TOP HEADER (Gradient Style) =====
        header = Frame(self, bg="#111827", height=80)
        header.pack(fill="x")

        Button(header, text="←",
               bg="#111827", fg="white",
               bd=0, font=("Segoe UI", 16),
               cursor="hand2",
               command=self.go_back).pack(side="left", padx=20)

        Label(header, text="PROFILE DASHBOARD",
              bg="#111827", fg="#E5E7EB",
              font=("Segoe UI", 16, "bold")).pack(side="left")

        # ===== MAIN CONTAINER =====
        container = Frame(self, bg="#0F172A")
        container.pack(fill="both", expand=True, padx=30, pady=30)

        # ===== LEFT PANEL =====
        left = Frame(container, bg="#111827", width=300)
        left.pack(side="left", fill="y", padx=(0, 20))

        # Profile Image
        img_path = self.user.get("face_image_path")

        if img_path and os.path.exists(img_path):
            img = Image.open(img_path)
            img = img.resize((120, 120))
            photo = ImageTk.PhotoImage(img)

            lbl = Label(left, image=photo, bg="#111827")
            lbl.image = photo
            lbl.pack(pady=25)
        else:
            Label(left, text="👤", font=("Segoe UI", 60),
                  bg="#111827", fg="white").pack(pady=25)

        name = f"{self.user.get('first_name')} {self.user.get('last_name')}"

        Label(left, text=name,
              bg="#111827", fg="white",
              font=("Segoe UI", 14, "bold")).pack()

        Label(left, text="AI Attendance User",
              bg="#111827", fg="#9CA3AF",
              font=("Segoe UI", 9)).pack(pady=5)

        # Buttons
        Button(left, text="Edit Profile",
               bg="#3B82F6", fg="white",
               bd=0, padx=20, pady=8,
               font=("Segoe UI", 10, "bold"),
               cursor="hand2",
               command=self.edit_profile).pack(pady=10)

        Button(left, text="Logout",
               bg="#EF4444", fg="white",
               bd=0, padx=20, pady=8,
               font=("Segoe UI", 10, "bold"),
               cursor="hand2",
               command=self.logout).pack()

     # ===== RIGHT PANEL =====
        right = Frame(container, bg="#0F172A")
        right.pack(side="left", fill="both", expand=True)

        # ===== STATS =====
        stats_frame = Frame(right, bg="#0F172A")
        stats_frame.pack(fill="x", pady=(0, 20))

        self.stat_card(stats_frame, "📅 Attendance", f"{stats['percentage']}%", 0)
        self.stat_card(stats_frame, "📊 Present Days", stats['present_days'], 1)
        self.stat_card(stats_frame, "📆 Total Days", stats['total_days'], 2)

        # ===== CHART CARD (MAIN FIX) =====
        chart_card = Frame(right, bg="#111827", bd=0)
        chart_card.pack(fill="both", expand=True, padx=10, pady=10)

        Label(chart_card, text="Attendance Analytics",
            bg="#111827", fg="white",
            font=("Segoe UI", 14, "bold")).pack(anchor="w", padx=15, pady=10)

        # Inner layout for charts
        charts_container = Frame(chart_card, bg="#111827")
        charts_container.pack(fill="both", expand=True)

        # LEFT = PIE
        pie_frame = Frame(charts_container, bg="#111827")
        pie_frame.pack(side="left", padx=10, pady=10)
        self.show_pie_chart(pie_frame)
        # RIGHT = BAR
        bar_frame = Frame(charts_container, bg="#111827")
        bar_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        self.show_bar_chart(bar_frame) 
                
            
                        
                
        
     # ===== STAT CARD =====
    def stat_card(self, parent, title, value, col):
        card = Frame(parent, bg="#111827", width=180, height=100)
        card.grid(row=0, column=col, padx=10)

        Label(card, text=title,
              bg="#111827", fg="#9CA3AF",
              font=("Segoe UI", 9)).pack(pady=10)

        Label(card, text=value,
              bg="#111827", fg="white",
              font=("Segoe UI", 16, "bold")).pack()

    # ===== DETAIL ROW =====
    def detail_row(self, parent, label, value):
        row = Frame(parent, bg="#111827")
        row.pack(fill="x", padx=20, pady=8)

        Label(row, text=label,
              bg="#111827", fg="#9CA3AF",
              width=15, anchor="w").pack(side="left")

        Label(row, text=value,
              bg="#111827", fg="white",
              font=("Segoe UI", 10, "bold")).pack(side="left")

    def go_back(self):
        self.destroy()

    def edit_profile(self):
        # Destroy current profile page widgets
        self.destroy()
        # Open Edit Profile page
        edit_page = EditProfilePage(self.root, self.user, self.main_app)
        
    def logout(self):
        self.main_app.logged_user = None
        self.main_app.build_ui()
   
    def show_pie_chart(self, parent):
        present, absent = db.get_attendance_summary(self.user.get("unique_id"))

        fig = plt.Figure(figsize=(3,3), dpi=100)
        ax = fig.add_subplot(111)

        ax.pie(
            [present, absent],
            labels=["Present", "Absent"],
            autopct='%1.1f%%',
            startangle=90
        )

        ax.set_facecolor("#111827")
        fig.patch.set_facecolor("#111827")

        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.draw()
        canvas.get_tk_widget().pack()
    def show_bar_chart(self, parent):
        dates = db.get_attendance_by_date(self.user.get("unique_id"))

        if not dates:
            Label(parent, text="No data", bg="#111827", fg="white").pack()
            return

        date_counts = {}
        for d in dates:
            date_counts[d] = date_counts.get(d, 0) + 1

        x = list(date_counts.keys())
        y = list(date_counts.values())

        fig = plt.Figure(figsize=(5,3), dpi=100)
        ax = fig.add_subplot(111)

        ax.bar(x, y)

        ax.set_title("Attendance Trend")
        ax.set_xlabel("Date")
        ax.set_ylabel("Days")

        ax.set_facecolor("#111827")
        fig.patch.set_facecolor("#111827")

        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)