from tkinter import messagebox
import tkinter as tk
from login import credentials, LoginPage


class SignupPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg="white")

        # Signup Form
        frame = tk.Frame(self, bg="white", bd=1, relief="solid", padx=20, pady=20)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(frame, text="Create Account", font=("Helvetica", 20, "bold"), bg="white", fg="black").pack(pady=(0, 10))
        tk.Label(frame, text="Username:", font=("Helvetica", 14), bg="white", fg="black").pack()
        self.entry_username = tk.Entry(frame, font=("Helvetica", 14))
        self.entry_username.pack()

        tk.Label(frame, text="Password:", font=("Helvetica", 14), bg="white", fg="black").pack()
        self.entry_password = tk.Entry(frame, font=("Helvetica", 14), show="*")
        self.entry_password.pack()

        tk.Button(frame, text="Create Account", command=self.create_account, font=("Helvetica", 16), fg="black", bg="white", width=25, height=2).pack(pady=10)

    def create_account(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        if username and password:
            # Add the new user to the credentials (In a real-world scenario, you'd add it to a database)
            credentials[username] = {"password": password, "role": "employee"}  # Default role as employee
            messagebox.showinfo("Account Created", f"Account for {username} has been created!")
            self.controller.show_frame("LoginPage")
        else:
            messagebox.showerror("Error", "Please fill in both fields")

