from tkinter import *
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk, ImageDraw
import os
import db

class EditProfilePage(Frame):
    def __init__(self, root, user, main_app):
        super().__init__(root, bg="#E5E7EB")  # soft gray background
        self.root = root
        self.user = user
        self.main_app = main_app
        self.face_image_path = user.get("face_image_path")
        self.place(x=0, y=0, relwidth=1, relheight=1)
        self.build_ui()

    def build_ui(self):
        card_size = 600  # square card

        # ===== SHADOW FRAME =====
        shadow = Frame(self, bg="#B0B0B0")
        shadow.place(relx=0.5, rely=0.5, anchor="center", width=card_size+10, height=card_size+10)

        # ===== MAIN CARD =====
        card = Frame(self, bg="white", bd=0, relief="ridge")
        card.place(relx=0.5, rely=0.5, anchor="center", width=card_size, height=card_size)

        # PROFILE IMAGE
        img_frame = Frame(card, bg="white")
        img_frame.pack(pady=20)
        self.img_label = Label(img_frame, bg="white")
        self.img_label.pack()
        self.load_profile_image(self.face_image_path)

        Button(img_frame, text="Change Photo", bg="#3B82F6", fg="white",
               bd=0, font=("Segoe UI", 10, "bold"), cursor="hand2",
               activebackground="#2563EB", command=self.upload_image).pack(pady=10)

        # INPUTS PANEL
        form = Frame(card, bg="white")
        form.pack(padx=40, pady=10, fill="both", expand=True)

        self.first_name_entry = self.create_input(form, "First Name", self.user.get("first_name"))
        self.middle_name_entry = self.create_input(form, "Middle Name", self.user.get("middle_name") or "")
        self.last_name_entry = self.create_input(form, "Last Name", self.user.get("last_name"))
        self.email_entry = self.create_input(form, "Email", self.user.get("email"))
        self.phone_entry = self.create_input(form, "Phone", self.user.get("phone"))

        # UPDATE BUTTON
        Button(card, text="Update Profile", bg="#10B981", fg="white",
               font=("Segoe UI", 12, "bold"), bd=0, pady=10,
               cursor="hand2", activebackground="#059669",
               command=self.update_profile).pack(pady=15)

    # ===== CREATE INPUT FIELD =====
    def create_input(self, parent, label_text, value=""):
        frame = Frame(parent, bg="white", height=50)
        frame.pack(fill="x", pady=6)
        Label(frame, text=label_text, bg="white", fg="#6B7280", font=("Segoe UI", 9)).pack(anchor="w")
        entry = Entry(frame, bd=1, font=("Segoe UI", 12), fg="#111827",
                      bg="#F9FAFB", insertbackground="black", relief="solid")
        entry.pack(fill="x", padx=5, pady=5)
        entry.insert(0, value)
        return entry

    # ===== PROFILE IMAGE =====
    def load_profile_image(self, path):
        if path and os.path.exists(path):
            img = Image.open(path).resize((100,100))
            img = self.make_circle(img)
            photo = ImageTk.PhotoImage(img)
            self.img_label.config(image=photo)
            self.img_label.image = photo
        else:
            self.img_label.config(text="👤", font=("Segoe UI", 60), fg="#111827")

    def make_circle(self, pil_img):
        size = pil_img.size
        mask = Image.new('L', size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0,0,size[0],size[1]), fill=255)
        result = Image.new('RGBA', size)
        result.paste(pil_img, (0,0), mask)
        return result

    def upload_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files","*.jpg *.jpeg *.png")])
        if file_path:
            self.face_image_path = file_path
            self.load_profile_image(file_path)

    # ===== UPDATE PROFILE =====
    def update_profile(self):
        uid = self.user.get("unique_id")
        first_name = self.first_name_entry.get().strip()
        middle_name = self.middle_name_entry.get().strip()
        last_name = self.last_name_entry.get().strip()
        email = self.email_entry.get().strip()
        phone = self.phone_entry.get().strip()
        try:
            conn = db.get_connection()
            cursor = conn.cursor()
            sql = "UPDATE user_registration SET first_name=%s, middle_name=%s, last_name=%s, email=%s, phone=%s"
            data = [first_name, middle_name or None, last_name, email, phone]
            if self.face_image_path:
                sql += ", face_image_path=%s"
                data.append(self.face_image_path)
            sql += " WHERE unique_id=%s"
            data.append(uid)
            cursor.execute(sql, tuple(data))
            conn.commit()
            cursor.close()
            conn.close()
            messagebox.showinfo("Success", "Profile updated successfully")
            self.main_app.logged_user = db.get_user_by_id(uid)
            self.go_back()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update profile: {e}")

    def go_back(self):
        self.destroy()