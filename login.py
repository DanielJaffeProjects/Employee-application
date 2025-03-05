import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk  # Import PIL library

try:
    import vlc  # Import VLC library
    vlc_available = True
except (ImportError, OSError):
    vlc_available = False

# Credentials dictionary mapping username to password and role
credentials = {
    "emp": {"password": "", "role": "employee"},
    "own": {"password": "", "role": "owner"},
    "man": {"password": "", "role": "manager"}
}

class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg="white")
        
        # Load the background image using PIL
        image = Image.open("clwbeach.jpg")
        self.bg_image = ImageTk.PhotoImage(image)
        self.bg_label = tk.Label(self, image=self.bg_image)
        self.bg_label.place(relwidth=1, relheight=1)

        # Initialize VLC player if available
        global vlc_available
        if vlc_available:
            try:
                self.player = vlc.MediaPlayer("Reggae Shark.mp4")
                self.player.audio_set_volume(100)  # Set volume to 100%
                self.player.play()
            except Exception as e:
                print(f"Error initializing VLC player: {e}")
                vlc_available = False

        # Centered frame for the login form with a subtle border
        frame = tk.Frame(self, bg="white", bd=1, relief="solid", padx=20, pady=20)
        frame.place(relx=0.5, rely=0.5, anchor="center")
        frame.configure(highlightbackground="white", highlightcolor="white", highlightthickness=1)

        # Header label
        tk.Label(frame, text="ALOHA", font=("Helvetica", 20, "bold"), bg="white", fg="black").pack(pady=(0, 10))

        # Username label and entry field
        tk.Label(frame, text="Username:", font=("Helvetica", 14), bg="white", fg="black").pack(pady=5)
        self.entry_username = tk.Entry(frame, font=("Helvetica", 14), width=25, bd=2, relief="solid")
        self.entry_username.pack(pady=5)

        # Password label and entry field
        tk.Label(frame, text="Password:", font=("Helvetica", 14), bg="white", fg="black").pack(pady=5)
        self.entry_password = tk.Entry(frame, font=("Helvetica", 14), show="*", width=25, bd=2, relief="solid")
        self.entry_password.pack(pady=5)

        # Login button with larger dimensions for easy clicking
        login_button = tk.Button(frame, text="Login", command=self.login, font=("Helvetica", 16), fg="black", bg="white", bd=2, relief="solid", width=25, height=2)
        login_button.pack(pady=20)

    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        
        if username in credentials and credentials[username]["password"] == password:
            if vlc_available:
                self.player.stop()  # Stop the audio when navigating away from the login screen
            role = credentials[username]["role"]
            if role == "employee":
                self.controller.show_frame("EmployeePage")
            elif role == "owner":
                self.controller.show_frame("OwnerPage")
            elif role == "manager":
                self.controller.show_frame("ManagerPage")
        else:
            messagebox.showerror("Login Failed", "Invalid Username or Password")
