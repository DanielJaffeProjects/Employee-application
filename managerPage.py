import tkinter as tk
from tkinter import messagebox, ttk
from manageEmployees import ManageEmployees

class ManagerPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg="white")

        self.manage_employees = ManageEmployees(self, controller)
        self.manage_employees.pack(expand=True, fill="both")
