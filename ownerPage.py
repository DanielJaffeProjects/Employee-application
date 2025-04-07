import tkinter as tk 
from managerPage import ManagerPage


class OwnerPage(ManagerPage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.controller = controller
        self.configure(bg="white")
//
