import tkinter as tk 
from managerPage import ManagerPage

class OwnerPage(ManagerPage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.controller = controller
        self.configure(bg="white")

        tk.Label(self, text="Owner Dashboard", font=("Helvetica", 20), bg="white").pack(pady=10)
