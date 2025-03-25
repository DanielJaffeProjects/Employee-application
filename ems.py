import tkinter as tk
from tkinter import messagebox
from login import LoginPage
from empPage import EmployeePage
from ownerPage import OwnerPage
from manageEmployees import ManageEmployees


class EMSApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("EMS Application")
        # made it full screen
        self.geometry("800x600")
        #todo put this back to normal
        # self.attributes("-fullscreen", True)
        self.configure(bg="white")

        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (LoginPage, EmployeePage, OwnerPage, ManageEmployees):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("LoginPage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

if __name__ == "__main__":
    app = EMSApp()
    app.mainloop()

