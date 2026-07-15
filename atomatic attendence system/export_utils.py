def export_attendance_csv(unique_id):
    import csv
    from tkinter import filedialog, messagebox
    import db

    file_path = filedialog.asksaveasfilename(
        defaultextension=".csv",
        filetypes=[("CSV files", "*.csv")],
        title="Save Attendance File"
    )

    if not file_path:
        return

    try:
        conn = db.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT 
                u.unique_id,
                CONCAT(u.first_name, ' ', u.last_name),
                u.email,
                u.phone,
                a.attendance_date,
                a.marked_at
            FROM attendance_logs a
            JOIN user_registration u 
                ON a.unique_id = u.unique_id
            WHERE a.unique_id = %s
            ORDER BY a.marked_at DESC
        """, (unique_id,))

        rows = cursor.fetchall()

        with open(file_path, mode="w", newline="") as file:
            writer = csv.writer(file)

            # HEADER
            writer.writerow(["User ID", "Name", "Email", "Phone", "Date", "Time"])

            # DATA
            for row in rows:
                uid, name, email, phone, date, time = row

                writer.writerow([
                    uid,
                    name,
                    email,
                    phone,
                    date.strftime("%Y-%m-%d"),
                    time.strftime("%H:%M:%S") if time else ""
                ])

        cursor.close()
        conn.close()

        messagebox.showinfo("Success", "Export completed ✅")

    except Exception as e:
        messagebox.showerror("Error", str(e))