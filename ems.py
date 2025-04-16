import tkinter as tk
from tkinter import messagebox

# Import your custom pages
import managerPage
from login import LoginPage
from empPage import EmployeePage
from ownerPage import OwnerPage
from OwnerAndManagerBase import ManageEmployees


class EMSApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("EMS Application")
        self.geometry("800x600")
        self.configure(bg="white")

        # Store session info
        self.employee_id = None
        self.role = None
        self.username = None

        # Container for all page frames
        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        # Dictionary to store instantiated frames
        self.frames = {}

        # Mapping page names to their classes for lazy loading
        self.page_classes = {
            "LoginPage": LoginPage,
            "EmployeePage": EmployeePage,
            "OwnerPage": OwnerPage,
            "ManageEmployees": ManageEmployees,
            "ManagerPage": managerPage.ManagerPage
        }

        # Load only the login page initially
        self.show_frame("LoginPage")

    def show_frame(self, page_name):
        # Lazy-load the frame if it doesn't exist yet
        if page_name not in self.frames:
            PageClass = self.page_classes.get(page_name)
            if PageClass:
                frame = PageClass(parent=self.container, controller=self)
                self.frames[page_name] = frame
                frame.grid(row=0, column=0, sticky="nsew")
            else:
                messagebox.showerror("Error", f"Page class '{page_name}' not found.")
                return

        frame = self.frames[page_name]
        frame.tkraise()

        # Reset geometry (optional, in case screen size changed)
        self.geometry("800x600")

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you really want to quit?"):
            self.destroy()


if __name__ == "__main__":
    app = EMSApp()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()
