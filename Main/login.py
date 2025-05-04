import os
import tkinter as tk

import pygame
from PIL import Image, ImageTk  # Import PIL for images

from Main.Notification import show_notification
from sqlConnector import connect

class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg="white")

        # Initialize pygame mixer for music
        pygame.mixer.init()

        # Load Background Image
        try:
            image_path = os.path.join(os.path.dirname(__file__), "../videos_and_pictures/clwbeach.jpg")
            image = Image.open(image_path)
            self.bg_image = ImageTk.PhotoImage(image)
            self.bg_label = tk.Label(self, image=self.bg_image)
            self.bg_label.place(relwidth=1, relheight=1)
        except FileNotFoundError:
            self.bg_label = tk.Label(self, text="Background Image Not Found", font=("Helvetica", 20), bg="white", fg="black")
            self.bg_label.place(relwidth=1, relheight=1)

        # Login Form
        frame = tk.Frame(self, bg="white", bd=1, relief="solid", padx=20, pady=20)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(frame, text="ALOHA", font=("Helvetica", 20, "bold"), bg="white", fg="black").pack(pady=(0, 10))
        tk.Label(frame, text="Username:", font=("Helvetica", 14), bg="white", fg="black").pack()
        self.entry_username = tk.Entry(frame, font=("Helvetica", 14))
        self.entry_username.pack()

        tk.Label(frame, text="Password:", font=("Helvetica", 14), bg="white", fg="black").pack()
        self.entry_password = tk.Entry(frame, font=("Helvetica", 14), show="*")
        self.entry_password.pack()

        tk.Button(frame, text="Login", command=self.login, font=("Helvetica", 16), fg="black", bg="white", width=25, height=2).pack(pady=10)

    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        query = "SELECT * FROM employee WHERE username = %s AND password = %s"

        user_data=connect(query, (username, password))
        print(user_data)

        if user_data and len(user_data)>0:
            user = user_data[0]
            print(user)
            role_index = 5
            role = user[role_index] if len(user) > role_index else None
            print(role)
            employee_id = user[0]
            if role:
                # Store session info in the controller
                print("Storing session info in controller")
                self.controller.employee_id = employee_id
                self.controller.role = role.title()
                self.controller.username = username


                # Play music for 30 seconds if the role is "Owner"
                if role.title() == "Owner":
                    self.play_music("Endi's Crazy Demands.mp3")  # 30 seconds

                if role.title() == "Manager":
                    self.play_music("Worst of the worst.mp3")

                if role.title() == "Employee":
                    self.play_music("Literal Chaos.mp3")

                # Show the appropriate page based on role
                self.controller.show_frame(f"{role.title()}Page")
            else:
                show_notification("User role not found.")
        else:
            show_notification( "Invalid Username or Password")

# play music
    def play_music(self, music_file, time=None):
        """Play background music once or stop it after a specified time."""
        try:
            # Construct the path to the music file in the videos_and_pictures folder
            music_path = os.path.join(os.path.dirname(__file__), "../videos_and_pictures", music_file)
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.play(loops=0)  # Play the file once
            if time is not None:
                self.after(time, pygame.mixer.music.stop)  # Stop music after the specified time
        except pygame.error as e:
            print(f"Error loading music: {e}")