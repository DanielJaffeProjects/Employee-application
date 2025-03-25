import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk  # Import PIL for images

from sqlConnector import connect

# User credentials (You can modify this to fetch from a database)
credentials = {
    "emp": {"password": "1234", "role": "employee"},
    "own": {"password": "1234", "role": "owner"},
    "man": {"password": "1234", "role": "manager"}
}

class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg="white")

        # Load Background Image
        try:
            image = Image.open("clwbeach.jpg")
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
            if role:
                role = role.title()
                self.controller.show_frame(f"{role}Page")
            else:
                messagebox.showerror("Login Failed", "User role not found.")
        else:
            messagebox.showerror("Login Failed", "Invalid Username or Password")