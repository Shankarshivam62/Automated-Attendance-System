from tkinter import *
from tkinter import messagebox
import sys
import login
import registration   # existing import kept
import features
import about
import blog
import faq
import contact
import help
import profile
import export_utils
import os

# Disable oneDNN optimization warnings
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

# Then import other libraries
import cv2

class LogFaceUI:

    def __init__(self, root):
        self.root = root
        self.logged_user = None
        self.root.geometry("1530x790+0+0")
        self.root.title("LogFace - Face Recognition Attendance System")
        self.root.configure(bg="white")
        self.menu_open = False
        
        # >>> ADDED
        self.registration_window = None
        self.build_ui()
        
    # ================= BUILD FULL UI =================

    def build_ui(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        # ================= NAVBAR =================
      
        # 1. ADD THE BLACK OVERLAY HERE (Add this right before the Side Menu code)
        # self.overlay = Label(self.root, bg="#000000") 
        self.overlay = Frame(self.root, bg="#ECE5E5")
        self.overlay.place_forget()  
        self.overlay.place(x=0, y=70, relwidth=1, relheight=1)
        self.overlay.attributes = 0.3   # (Tkinter has limitation here)
        # ================= SIDE MENU =================
        self.side_menu = Frame(self.root, bg="white", width=300)
        self.side_menu.place(x=-300, y=70, height=720)

        profile = Frame(self.side_menu, bg="white")
        profile.pack(pady=25)

        Label(profile, text="👤", bg="white", font=("Segoe UI", 45)).pack()
        # 👤 User name (dynamic)
        user_name = "Guest"
        user_role = "Student"

        if self.logged_user:
            user_name = self.logged_user.get("first_name", "User")
            user_role = "Logged In"

        Label(
            profile,
            text=user_name,
            bg="white",
            fg="#111827",
            font=("Segoe UI", 14, "bold")
        ).pack()

        Label(
            profile,
            text=user_role,
            bg="white",
            fg="#6B7280",
            font=("Segoe UI", 10)
        ).pack()

        # 2. ADD THE PROFILE BUTTON HERE
        Button(profile, text="View Profile", bg="#F9F8FA", fg="white", 
               font=("Segoe UI", 9), bd=0, padx=10, cursor="hand2",
               command=self.open_profile).pack(pady=5)

        Button(profile, text="Logout", bg="white", fg="red", bd=0, 
               cursor="hand2", command=self.logout).pack(pady=5)
        
        # ... (rest of your menu buttons)
      
      
        navbar = Frame(self.root, bg="white", height=70)

        navbar.pack(fill="x")

        Button(
            navbar,
            text="☰",
            bg="white",
            fg="#111827",
            font=("Segoe UI", 18, "bold"),
            bd=0,
            cursor="hand2",
            command=self.toggle_menu
        ).pack(side="left", padx=20)
        
        Button(
            navbar,
            text="🔷 LogFace",
            bg="white",
            fg="#111827",
            font=("Segoe UI", 20, "bold"),
            bd=0,
            cursor="hand2",
            activebackground="white",
            command=self.build_ui
        ).pack(side="left", padx=10)
        
        menu_frame = Frame(navbar, bg="white")
        menu_frame.pack(side="left", padx=120)
        self.create_nav_button(menu_frame, "Features", self.open_features)
        self.create_nav_button(menu_frame, "About Us", self.open_about)  
        self.create_nav_button(menu_frame, "Blog", self.open_blog)       
        self.create_nav_button(menu_frame, "FAQ's", self.open_faq)      
        self.create_nav_button(menu_frame, "Contact Sales", self.open_contact)   
        self.create_nav_button(menu_frame, "Help", self.open_help)
        
        right_frame = Frame(navbar, bg="white")
        right_frame.pack(side="right", padx=40)



        Button(

            right_frame,
            text="⏻ Exit",
            bg="white",
            fg="#DC2626",
            font=("Segoe UI", 11, "bold"),
            bd=0,
            cursor="hand2",
            command=self.exit_app
        ).pack(side="right", padx=15)      
       
        Button(
            right_frame,
            text="Register",
            bg="#374151",
            fg="white",
            font=("Segoe UI", 11, "bold"),
            bd=0,
            padx=18,
            pady=6,
            cursor="hand2",
            command=self.open_register
        ).pack(side="right", padx=10)

        Button(
            right_frame,
            text="Login",
            bg="#F3F4F6",
            fg="#111827",
            font=("Segoe UI", 11, "bold"),
            bd=0,
            padx=18,
            pady=6,
            cursor="hand2",
            command=self.open_login
        ).pack(side="right", padx=10)

       
        # ================= SIDE MENU =================
        Label(self.side_menu,
              text="ATTENDANCE",
              bg="white",
              fg="#6B7280",
              font=("Segoe UI", 9, "bold")).pack(anchor="w", padx=20)
        self.menu_button("✅ Mark Attendance", self.mark_attendance)
        self.menu_button("📋 Attendance History", self.attendance_history)
        self.menu_button("📈 Attendance Graph", self.attendance_graph)
        self.menu_button("📁 Export Attendance (CSV)", self.export_attendance)

        Label(self.side_menu,
              text="SYSTEM",
              bg="white",
              fg="#6B7280",
              font=("Segoe UI", 9, "bold")).pack(anchor="w", padx=20, pady=(20, 0))
        self.menu_button("🔐 Change Password", self.change_password)
        self.menu_button("🎥 Camera Settings", self.camera_settings)
        self.menu_button("🌙 Dark/Light Mode", self.toggle_theme)
        self.menu_button("🗑 Delete Account", self.delete_account)
        # ================= HERO =================
        hero = Frame(self.root, bg="#1E88C8", height=420)
        hero.pack(fill="x")
        Label(
            hero,
            text="Imagine your new Time & Attendance Tracking website",
            bg="#1E88C8",
            fg="white",
            font=("Segoe UI", 30, "bold")
        ).pack(pady=100)

        Label(
            hero,
            text="Modern • Secure • AI Powered Face Recognition System",
            bg="#1E88C8",
            fg="white",
            font=("Segoe UI", 14)
        ).pack()
   # ================= NAVIGATION =================

    def open_register(self):
        # Prevent opening multiple registration frames
        if hasattr(self, "registration_frame") and self.registration_frame.winfo_exists():
            return
        # Passing 'self' allows the registration page to talk back to this file

        self.registration_frame = registration.App(self.root, main_app=self)
        width = self.root.winfo_width()

        self.registration_frame.place(x=width, y=0, relwidth=1, relheight=1)
        # Slide animation

        def slide():
            if not hasattr(self, "registration_frame"): return
            x = self.registration_frame.winfo_x()
            if x <= 0:
                self.registration_frame.place(x=0, y=0)
                return
            self.registration_frame.place(x=x - 40, y=0)
            self.root.after(10, slide)
            
        slide()
    def return_to_main(self):
        if not hasattr(self, "registration_frame"):
            return
        width = self.root.winfo_width()
        def slide_back():
            if not hasattr(self, "registration_frame") or not self.registration_frame.winfo_exists():
                return
            x = self.registration_frame.winfo_x()
            if x >= width:
                self.registration_frame.destroy()
                del self.registration_frame
                return
            self.registration_frame.place(x=x + 40, y=0)
            self.root.after(10, slide_back)
        slide_back()

    # >>> ADDED

    def fade_in(self, win):
        alpha = win.attributes("-alpha")
        if alpha < 1:
            win.attributes("-alpha", alpha + 0.05)
            win.after(10, lambda: self.fade_in(win))

    # >>> ADDED
    def close_registration(self):
        if not self.registration_window:
            return
        self.fade_out(self.registration_window)

    # >>> ADDED

    def fade_out(self, win):
        alpha = win.attributes("-alpha")
        if alpha > 0:
            win.attributes("-alpha", alpha - 0.05)
            win.after(10, lambda: self.fade_out(win))
        else:
            win.destroy()
            self.registration_window = None
    # ================= HELPERS =================
    def toggle_menu(self):
        if self.menu_open:
            self.side_menu.place(x=-300, y=70)
            self.menu_open = False
        else:
            self.overlay.place(x=0, y=70, relwidth=1, relheight=1)
            self.side_menu.place(x=0, y=70)
            self.side_menu.lift()
            self.menu_open = True
    def menu_button(self, text, command):
        Button(self.side_menu, text=text, bg="white", fg="#111827",
               font=("Segoe UI", 11), bd=0, anchor="w",
               padx=25, pady=8, cursor="hand2",
               command=command).pack(fill="x")

    def mark_attendance(self):
    # Open the new attendance window
     from mark_attendance import MarkAttendanceApp
     MarkAttendanceApp(self.root)

    def attendance_history(self):
        if not self.logged_user:
            messagebox.showwarning("Login Required", "Please login first")
            return
        from attendance_details import AttendanceDetailsPage
        AttendanceDetailsPage(self.root, self.logged_user)
        
    def attendance_graph(self): messagebox.showinfo("Graph", "Attendance Graph")
   
    def export_attendance(self):
        if not self.logged_user:
            from tkinter import messagebox
            messagebox.showwarning("Login Required", "Please login first")
            return

        unique_id = self.logged_user.get("unique_id")
        export_utils.export_attendance_csv(unique_id)
    
    def change_password(self): messagebox.showinfo("Password", "Change Password")
    def camera_settings(self): messagebox.showinfo("Camera", "Camera Settings")
    def toggle_theme(self): messagebox.showinfo("Theme", "Toggle Theme")
    def delete_account(self): messagebox.showwarning("Delete", "Delete Account")
    def logout(self):
        confirm = messagebox.askyesno("Logout", "Are you sure you want to logout?")
        if not confirm:
            return

        # ✅ 1. Clear session
        self.logged_user = None

        # ✅ 2. Destroy ALL dynamic frames safely
        for attr in list(vars(self).keys()):
            obj = getattr(self, attr)

            try:
                if hasattr(obj, "winfo_exists") and obj.winfo_exists():
                    obj.destroy()
            except:
                pass

        # ✅ 3. Close OpenCV windows (VERY IMPORTANT)
        try:
            import cv2
            cv2.destroyAllWindows()
        except:
            pass

        # ✅ 4. Rebuild clean UI (Guest mode)
        self.build_ui()

      
    def create_nav_button(self, parent, text, command=None):

        Button(parent, text=text, bg="white", fg="#374151",
               font=("Segoe UI", 11), bd=0, cursor="hand2",
               activebackground="white",
               activeforeground="#2563EB",
               command=command).pack(side="left", padx=18)
    def return_to_main(self):

        # Check if the registration frame exists

        if not hasattr(self, "registration_frame") or not self.registration_frame.winfo_exists():
            return   
        width = self.root.winfo_width()
        def slide_back():
            # Get current X position

            current_x = self.registration_frame.winfo_x()  
            # If it has moved off-screen to the right, destroy it
            if current_x >= width:
                self.registration_frame.destroy()
                # Clean up the reference
                if hasattr(self, "registration_frame"):
                    del self.registration_frame
                return
            # Move the frame 40 pixels to the right

            self.registration_frame.place(x=current_x + 40, y=0)

            # Repeat after 10ms for smooth motion

            self.root.after(10, slide_back)

        slide_back()

    def show_help(self):

        messagebox.showinfo("Help", "Automatic Attendance System")

    def exit_app(self):
        if messagebox.askyesno("Exit", "Are you sure?"):
            self.root.destroy()
            import db
        print("DB FILE:", db.__file__)
        db.cleanup_orphan_faces()
        
    def open_login(self):
    
        if hasattr(self, "login_frame") and self.login_frame.winfo_exists():
            return
        self.login_frame = login.LoginApp(self.root, main_app=self)
        width = self.root.winfo_width()
        self.login_frame.place(x=width, y=0, relwidth=1, relheight=1)
        # slide animation
        def slide():
            x = self.login_frame.winfo_x()
            if x <= 0:
                self.login_frame.place(x=0, y=0)
                return
            self.login_frame.place(x=x - 40, y=0)
            self.root.after(10, slide)
        slide()
    def open_features(self):
        if hasattr(self, "features_frame") and self.features_frame.winfo_exists():
            return

        self.features_frame = features.FeaturesPage(self.root, main_app=self)
        width = self.root.winfo_width()
        self.features_frame.place(x=width, y=0, relwidth=1, relheight=1)

        def slide():
            x = self.features_frame.winfo_x()
            if x <= 0:
                self.features_frame.place(x=0, y=0)
                return
            self.features_frame.place(x=x - 40, y=0)
            self.root.after(10, slide)

        slide()
        
    def return_from_features(self):
        if not hasattr(self, "features_frame") or not self.features_frame.winfo_exists():
            return

        width = self.root.winfo_width()

        def slide_back():
            x = self.features_frame.winfo_x()
            if x >= width:
                self.features_frame.destroy()
                del self.features_frame
                return

            self.features_frame.place(x=x + 40, y=0)
            self.root.after(10, slide_back)

        slide_back()
        
    def open_about(self):
        if hasattr(self, "about_frame") and self.about_frame.winfo_exists():
            return

        self.about_frame = about.AboutPage(self.root, main_app=self)

        width = self.root.winfo_width()
        self.about_frame.place(x=width, y=0, relwidth=1, relheight=1)

        def slide():
            x = self.about_frame.winfo_x()
            if x <= 0:
                self.about_frame.place(x=0, y=0)
                return
            self.about_frame.place(x=x - 40, y=0)
            self.root.after(10, slide)

        slide()
        
        
        
    def return_from_about(self):
        if not hasattr(self, "about_frame") or not self.about_frame.winfo_exists():
            return

        width = self.root.winfo_width()

        def slide_back():
            x = self.about_frame.winfo_x()
            if x >= width:
                self.about_frame.destroy()
                del self.about_frame
                return

            self.about_frame.place(x=x + 40, y=0)
            self.root.after(10, slide_back)

        slide_back()
        
    def open_blog(self):
        if hasattr(self, "blog_frame") and self.blog_frame.winfo_exists():
            return
        self.blog_frame = blog.BlogPage(self.root, main_app=self)
        self.blog_frame.place(x=0, y=0, relwidth=1, relheight=1)
        
    def open_faq(self):
        if hasattr(self, "faq_frame") and self.faq_frame.winfo_exists():
            return

        self.faq_frame = faq.FAQPage(self.root, main_app=self)
        self.faq_frame.place(x=0, y=0, relwidth=1, relheight=1)    
        
    def return_from_faq(self):
        if hasattr(self, "faq_frame"):
            self.faq_frame.destroy()
            
    def open_contact(self):
        if hasattr(self, "contact_frame") and self.contact_frame.winfo_exists():
         return

        self.contact_frame = contact.ContactPage(self.root, main_app=self)
        self.contact_frame.place(x=0, y=0, relwidth=1, relheight=1)        
    
    def return_from_contact(self):
        if hasattr(self, "contact_frame"):
            self.contact_frame.destroy()
            
    # Open Help Page
    def open_help(self):
        if hasattr(self, "help_frame") and self.help_frame.winfo_exists():
            return
        self.help_frame = help.HelpPage(self.root, main_app=self)
        width = self.root.winfo_width()
        self.help_frame.place(x=width, y=0, relwidth=1, relheight=1)

        # Slide-in animation
        def slide():
            x = self.help_frame.winfo_x()
            if x <= 0:
                self.help_frame.place(x=0, y=0)
                return
            self.help_frame.place(x=x - 40, y=0)
            self.root.after(10, slide)
        slide()

    # Return from Help Page
    def return_from_help(self):
        if not hasattr(self, "help_frame") or not self.help_frame.winfo_exists():
            return
        width = self.root.winfo_width()
        def slide_back():
            x = self.help_frame.winfo_x()
            if x >= width:
                self.help_frame.destroy()
                del self.help_frame
                return
            self.help_frame.place(x=x + 40, y=0)
            self.root.after(10, slide_back)
        slide_back()
    def open_profile(self):
        if not self.logged_user:
            messagebox.showwarning("Login Required", "Please login first")
            return
        profile.ProfilePage(self.root, self.logged_user, self)    
            
if __name__ == "__main__":
    root = Tk()
    app = LogFaceUI(root)
    root.mainloop()
    
    