import tkinter as tk
import login

class EmployeePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg="white")

        # Left frame for custom tabs with a subtle border
        tab_frame = tk.Frame(self, bg="white", width=220, bd=1, relief="solid")
        tab_frame.pack(side="left", fill="y", padx=10, pady=10)

        # Right frame for tab content with a subtle border
        content_frame = tk.Frame(self, bg="white", bd=1, relief="solid")
        content_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        content_frame.grid_rowconfigure(0, weight=1)
        content_frame.grid_columnconfigure(0, weight=1)

        # Define the tabs and create a corresponding frame for each tab
        tabs = {}
        tab_titles = [
            "Enter Expense", 
            "Enter Employee Withdrawal", 
            "Enter Day Closeout", 
            "Enter Bonus"
        ]

        for title in tab_titles:
            frame = tk.Frame(content_frame, bg="white")
            frame.grid(row=0, column=0, sticky="nsew")
            tk.Label(
                frame, 
                text=title, 
                font=("Helvetica", 18), 
                bg="white", 
                fg="black"
            ).pack(pady=40)
            tabs[title] = frame

        # Function to show the selected tab's content
        def show_tab(tab_name):
            tabs[tab_name].tkraise()

        # Create a button for each tab in the left frame with larger dimensions
        for title in tab_titles:
            btn = tk.Button(
                tab_frame, 
                text=title, 
                font=("Helvetica", 14), 
                fg="black", 
                bg="white", 
                relief="flat", 
                bd=2, 
                command=lambda t=title: show_tab(t),
                width=25,
                height=3
            )
            btn.pack(fill="x", pady=5, padx=10)

        # Logout button at the bottom of the left frame with larger dimensions
        logout_button = tk.Button(
            tab_frame, 
            text="Logout", 
            font=("Helvetica", 14), 
            fg="black", 
            bg="white", 
            relief="flat", 
            bd=2, 
            command=lambda: controller.show_frame("LoginPage"),
            width=25,
            height=3
        )
        logout_button.pack(side="bottom", pady=10, padx=10)

        # Display the first tab by default
        show_tab(tab_titles[0])

if __name__ == '__main__':
    root = tk.Tk()
    root.title("Dashboard")
    root.geometry("900x750")
    root.configure(bg="white")
    employee_page = EmployeePage(root, None)
    employee_page.pack(fill="both", expand=True)
    root.mainloop()
