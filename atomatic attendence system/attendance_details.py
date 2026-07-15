# attendance_details.py
import tkinter as tk
from tkinter import ttk
import mysql.connector
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import datetime

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "Sitaram620@",
    "database": "logface"
}

class AttendanceDetailsPage(tk.Frame):

    def __init__(self, root, user):
        super().__init__(root)
        self.root = root
        self.user = user
        self.unique_id = user["unique_id"]
        self.place(x=0, y=0, relwidth=1, relheight=1)
        self.build_ui()

    # ---------------- DB ----------------
    def get_conn(self):
        return mysql.connector.connect(**DB_CONFIG)
    
    
    def draw_monthly_chart(self):
        conn = self.get_conn()
        cur = conn.cursor()

        cur.execute("""
            SELECT MONTH(attendance_date), COUNT(*)
            FROM attendance_logs
            WHERE unique_id = %s
            GROUP BY MONTH(attendance_date)
            ORDER BY MONTH(attendance_date)
        """, (self.unique_id,))

        rows = cur.fetchall()
        cur.close()
        conn.close()

        if not rows:
            tk.Label(self.month_chart_frame, text="No Data").pack()
            return

        months = [r[0] for r in rows]
        present = [r[1] for r in rows]

        fig = plt.Figure(figsize=(4, 3), dpi=100)
        ax = fig.add_subplot(111)

        ax.bar(months, present)
        ax.set_title("Monthly Attendance")
        ax.set_xlabel("Month")
        ax.set_ylabel("Days Present")

        canvas = FigureCanvasTkAgg(fig, self.month_chart_frame)
        canvas.get_tk_widget().pack(fill="both", expand=True)
        canvas.draw()

        # ---------------- UI ----------------
    def build_ui(self):

        title = tk.Label(
            self, text="Attendance Dashboard",
            font=("Segoe UI", 22, "bold"),
            bg="#f4f6f9"
        )
        title.pack(pady=10)

        # ===== CARDS =====
        cards = tk.Frame(self, bg="#f4f6f9")
        cards.pack(fill="x", padx=30)

        self.card_total = self.create_card(cards, "TOTAL", "#3498db")
        self.card_present = self.create_card(cards, "PRESENT", "#2ecc71")
        self.card_absent = self.create_card(cards, "ABSENT", "#e74c3c")
        self.card_late = self.create_card(cards, "LATE", "#f39c12")

        # ===== CONTENT =====
        body = tk.Frame(self, bg="#f4f6f9")
        body.pack(fill="both", expand=True, padx=20, pady=10)

        # CHART
        self.chart_frame = tk.Frame(body, bg="white")
        self.chart_frame.pack(side="left", fill="both", expand=True, padx=10)

        self.draw_chart()

        # TABLE
        table_frame = tk.Frame(body, bg="white")
        table_frame.pack(side="right", fill="both", expand=True, padx=10)

        self.table = ttk.Treeview(
            table_frame,
            columns=("ID", "Date", "Time"),
            show="headings"
        )

        for col in ("ID", "Date", "Time"):
            self.table.heading(col, text=col)
            self.table.column(col, anchor="center")

        self.table.pack(fill="both", expand=True)
        
        charts_container = tk.Frame(self, bg="#f4f6f9")
        charts_container.pack(fill="both", expand=True, padx=15, pady=15)

        # DAILY / MAIN CHART
        self.chart_frame = tk.Frame(charts_container, bg="white")
        self.chart_frame.pack(side="left", fill="both", expand=True, padx=10)

        # MONTHLY CHART
        self.month_chart_frame = tk.Frame(charts_container, bg="white")
        self.month_chart_frame.pack(side="left", fill="both", expand=True, padx=10)

        # DRAW CHARTS
        self.draw_monthly_chart()
        self.table = ttk.Treeview(
            self,
            columns=("ID", "Date", "Time"),
            show="headings",
            height=12
        )
        self.table.heading("ID", text="User ID")
        self.table.heading("Date", text="Date")
        self.table.heading("Time", text="Time")
        self.table.pack(fill="both", expand=True, padx=20, pady=10)
        # LOAD ONLY LOGGED USER DATA
        self.load_attendance_from_db()

    # ---------------- CARD ----------------
    def create_card(self, parent, title, color):
        frame = tk.Frame(parent, bg=color, height=90)
        frame.pack(side="left", expand=True, fill="x", padx=8)

        lbl_title = tk.Label(
            frame, text=title, bg=color,
            fg="white", font=("Segoe UI", 10, "bold")
        )
        lbl_title.pack(pady=(10, 0))

        lbl_value = tk.Label(
            frame, text="0", bg=color,
            fg="white", font=("Segoe UI", 22, "bold")
        )
        lbl_value.pack()

        return lbl_value

    # ---------------- SUMMARY ----------------
    def load_summary(self):
        conn = self.get_conn()
        cur = conn.cursor()

        # Present days (for this user)
        cur.execute("""
            SELECT COUNT(DISTINCT attendance_date)
            FROM attendance_logs
            WHERE unique_id = %s
        """, (self.unique_id,))
        
        result = cur.fetchone()
        present = result[0] if result and result[0] is not None else 0

        # Total days since registration
        cur.execute("""
            SELECT DATEDIFF(CURDATE(), registered_at)
            FROM user_registration
            WHERE unique_id = %s
        """, (self.unique_id,))
        
        result = cur.fetchone()
        total = result[0] if result and result[0] is not None else 1
        absent = max(0, total - present)
        late = 0
        # Update UI
        self.card_total.config(text=total)
        self.card_present.config(text=present)
        self.card_absent.config(text=absent)
        self.card_late.config(text=late)

        cur.close()
        conn.close()
        
    def load_attendance_from_db(self):
        conn = self.get_conn()
        cur = conn.cursor()
        cur.execute("""
            SELECT attendance_date, marked_at
            FROM attendance_logs
            WHERE unique_id = %s
            ORDER BY marked_at DESC
        """, (self.unique_id,))
        rows = cur.fetchall()
        cur.close()
        conn.close()
        self.table.delete(*self.table.get_children())
        for date, time in rows:
            self.table.insert("", "end", values=(
                self.unique_id,
                date,
                time.strftime("%H:%M:%S")
            ))    

    # ---------------- TABLE ----------------
    def load_table(self):
        self.table.delete(*self.table.get_children())
        conn = self.get_conn()
        cur = conn.cursor()

        cur.execute(
            "SELECT unique_id, attendance_date, marked_at FROM attendance_logs ORDER BY marked_at DESC LIMIT 50"
        )

        for row in cur.fetchall():
            self.table.insert("", "end", values=row)

        cur.close()
        conn.close()

    # ---------------- CHART ----------------
    def draw_chart(self):
        conn = self.get_conn()
        cur = conn.cursor()

        # Total days user attended
        cur.execute("""
            SELECT COUNT(DISTINCT attendance_date)
            FROM attendance_logs
            WHERE unique_id = %s
        """, (self.unique_id,))
        present = cur.fetchone()[0] or 0

        # Total possible days
        cur.execute("""
            SELECT DATEDIFF(CURDATE(), registered_at)
            FROM user_registration
            WHERE unique_id = %s
        """, (self.unique_id,))
        total = cur.fetchone()[0] or 1

        absent = max(0, total - present)

        cur.close()
        conn.close()

        fig = plt.Figure(figsize=(4, 4), dpi=100)
        ax = fig.add_subplot(111)

        ax.pie(
            [present, absent],
            labels=["Present", "Absent"],
            autopct="%1.1f%%",
            startangle=90
        )

        ax.set_title("Attendance Overview")

        canvas = FigureCanvasTkAgg(fig, self.chart_frame)
        canvas.get_tk_widget().pack(fill="both", expand=True)
        canvas.draw()
        self.load_summary()