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
        
        # Tab: Enter Expense
        expense_frame = tk.Frame(content_frame, bg="white")
        expense_frame.grid(row=0, column=0, sticky="nsew")
        tk.Label(expense_frame, text="Enter Expense", font=("Helvetica", 18), bg="white", fg="black").pack(pady=10)
        tk.Label(expense_frame, text="Expense ID:", font=("Helvetica", 14), bg="white", fg="black").pack(pady=5)
        expense_id = tk.Entry(expense_frame, font=("Helvetica", 14))
        expense_id.pack(pady=5)
        tk.Label(expense_frame, text="Date (YYYY-MM-DD):", font=("Helvetica", 14), bg="white", fg="black").pack(pady=5)
        expense_date = tk.Entry(expense_frame, font=("Helvetica", 14))
        expense_date.pack(pady=5)
        tk.Label(expense_frame, text="Amount:", font=("Helvetica", 14), bg="white", fg="black").pack(pady=5)
        expense_amount = tk.Entry(expense_frame, font=("Helvetica", 14))
        expense_amount.pack(pady=5)
        tk.Label(expense_frame, text="Category:", font=("Helvetica", 14), bg="white", fg="black").pack(pady=5)
        expense_category = tk.Entry(expense_frame, font=("Helvetica", 14))
        expense_category.pack(pady=5)
        tk.Button(expense_frame, text="Submit Expense", font=("Helvetica", 14),
                  command=lambda: messagebox.showinfo("Expense", "Expense Submitted")).pack(pady=10)
        tabs["Enter Expense"] = expense_frame
        
        # Tab: Enter Employee Withdrawal
        withdrawal_frame = tk.Frame(content_frame, bg="white")
        withdrawal_frame.grid(row=0, column=0, sticky="nsew")
        tk.Label(withdrawal_frame, text="Enter Employee Withdrawal", font=("Helvetica", 18), bg="white", fg="black").pack(pady=10)
        tk.Label(withdrawal_frame, text="Withdrawal ID:", font=("Helvetica", 14), bg="white", fg="black").pack(pady=5)
        withdrawal_id = tk.Entry(withdrawal_frame, font=("Helvetica", 14))
        withdrawal_id.pack(pady=5)
        tk.Label(withdrawal_frame, text="Date (YYYY-MM-DD):", font=("Helvetica", 14), bg="white", fg="black").pack(pady=5)
        withdrawal_date = tk.Entry(withdrawal_frame, font=("Helvetica", 14))
        withdrawal_date.pack(pady=5)
        tk.Label(withdrawal_frame, text="Amount:", font=("Helvetica", 14), bg="white", fg="black").pack(pady=5)
        withdrawal_amount = tk.Entry(withdrawal_frame, font=("Helvetica", 14))
        withdrawal_amount.pack(pady=5)
        tk.Button(withdrawal_frame, text="Submit Withdrawal", font=("Helvetica", 14),
                  command=lambda: messagebox.showinfo("Withdrawal", "Withdrawal Submitted")).pack(pady=10)
        tabs["Enter Employee Withdrawal"] = withdrawal_frame
        
        # Tab: Enter Day Closeout
        closeout_frame = tk.Frame(content_frame, bg="white")
        closeout_frame.grid(row=0, column=0, sticky="nsew")
        tk.Label(closeout_frame, text="Enter Day Closeout", font=("Helvetica", 18), bg="white", fg="black").pack(pady=10)
        tk.Label(closeout_frame, text="Date (YYYY-MM-DD):", font=("Helvetica", 14), bg="white", fg="black").pack(pady=5)
        closeout_date = tk.Entry(closeout_frame, font=("Helvetica", 14))
        closeout_date.pack(pady=5)
        tk.Label(closeout_frame, text="Total Sales:", font=("Helvetica", 14), bg="white", fg="black").pack(pady=5)
        total_sales = tk.Entry(closeout_frame, font=("Helvetica", 14))
        total_sales.pack(pady=5)
        tk.Label(closeout_frame, text="Closing Cash Amount:", font=("Helvetica", 14), bg="white", fg="black").pack(pady=5)
        closing_cash = tk.Entry(closeout_frame, font=("Helvetica", 14))
        closing_cash.pack(pady=5)
        tk.Button(closeout_frame, text="Submit Closeout", font=("Helvetica", 14),
                  command=lambda: messagebox.showinfo("Day Closeout", "Day Closeout Completed")).pack(pady=10)
        tabs["Enter Day Closeout"] = closeout_frame
        
        # Tab: Enter Bonus
        bonus_frame = tk.Frame(content_frame, bg="white")
        bonus_frame.grid(row=0, column=0, sticky="nsew")
        tk.Label(bonus_frame, text="Enter Bonus", font=("Helvetica", 18), bg="white", fg="black").pack(pady=10)
        tk.Label(bonus_frame, text="Sales Amount:", font=("Helvetica", 14), bg="white", fg="black").pack(pady=5)
        bonus_sales = tk.Entry(bonus_frame, font=("Helvetica", 14))
        bonus_sales.pack(pady=5)
        tk.Label(bonus_frame, text="Bonus Percentage:", font=("Helvetica", 14), bg="white", fg="black").pack(pady=5)
        bonus_pct = tk.Entry(bonus_frame, font=("Helvetica", 14))
        bonus_pct.pack(pady=5)
        
        def calculate_bonus():
            try:
                sales = float(bonus_sales.get())
                percent = float(bonus_pct.get())
                bonus = sales * percent / 100
                messagebox.showinfo("Bonus", f"Calculated Bonus: {bonus:.2f}")
            except ValueError:
                messagebox.showerror("Error", "Please enter valid numbers for Sales Amount and Bonus Percentage")
                
        tk.Button(bonus_frame, text="Calculate Bonus", font=("Helvetica", 14),
                  command=calculate_bonus).pack(pady=10)
        tabs["Enter Bonus"] = bonus_frame
        
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
