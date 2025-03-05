import tkinter as tk
from tkinter import messagebox
import login

class EmployeePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg="white")
        
        # Left frame for tab buttons
        tab_frame = tk.Frame(self, bg="white", width=220, bd=1, relief="solid")
        tab_frame.pack(side="left", fill="y", padx=10, pady=10)
        
        # Right frame for content
        content_frame = tk.Frame(self, bg="white", bd=1, relief="solid")
        content_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        content_frame.grid_rowconfigure(0, weight=1)
        content_frame.grid_columnconfigure(0, weight=1)
        
        # Dictionary to hold the tabs and their corresponding frames
        tabs = {}

        # clock in and enter register in balance
        reg_in = tk.Frame(content_frame, bg="white")
        reg_in.grid(row=0, column=0, sticky="nsew")
        tk.Label(reg_in, text="Enter Reg-In Balance", font=("Helvetica", 18), bg="white", fg="black").pack(
            pady=10)
        reg_in_balance = tk.Entry(reg_in, font=("Helvetica", 14))
        reg_in_balance.pack(pady=5)
        tk.Button(reg_in, text="Submit and clock in", font=("Helvetica", 14),
                  command=lambda: messagebox.showinfo("balance", "balance Submitted")).pack(pady=10)
        tabs["Clock in"] = reg_in

        # clock out and enter register out balance
        reg_out = tk.Frame(content_frame, bg="white")
        reg_out.grid(row=0, column=0, sticky="nsew")
        tk.Label(reg_out, text="Enter Reg-Out Balance", font=("Helvetica", 18), bg="white", fg="black").pack(
            pady=10)
        reg_out_balance = tk.Entry(reg_out, font=("Helvetica", 14))
        reg_out_balance.pack(pady=5)
        tk.Button(reg_out, text="Submit and clock out", font=("Helvetica", 14),
                  command=lambda: messagebox.showinfo("balance", " balance submitted ")).pack(pady=10)
        tabs["Clock out"] = reg_out




        # Function to switch tabs
        def show_tab(tab_name):
            tabs[tab_name].tkraise()

        # Create tab buttons
        tab_titles = list(tabs.keys())
        for title in tab_titles:
            btn = tk.Button(tab_frame, text=title, font=("Helvetica", 14), fg="black", bg="white",
                            relief="flat", bd=2, command=lambda t=title: show_tab(t), width=25, height=3)
            btn.pack(pady=5, padx=10, fill="x")

        # Logout button at the bottom of the tab frame
        logout_button = tk.Button(tab_frame, text="Logout", font=("Helvetica", 14), fg="black", bg="white",
                                  relief="flat", bd=2, command=lambda: controller.show_frame("LoginPage"),
                                  width=25, height=3)
        logout_button.pack(side="bottom", pady=10, padx=10)

        # Show the default tab (Enter Expense)
        show_tab(tab_titles[0])

if __name__ == '__main__':
    root = tk.Tk()
    root.title("Employee Dashboard")
    root.geometry("900x750")
    employee_page = EmployeePage(root, None)
    employee_page.pack(fill="both", expand=True)
    root.mainloop()
