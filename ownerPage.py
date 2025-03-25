import tkinter as tk 
from managerPage import ManageEmployees

class OwnerPage(ManageEmployees):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.controller = controller
        self.configure(bg="white")

