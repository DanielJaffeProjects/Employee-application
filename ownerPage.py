import tkinter as tk
from tkinter import messagebox
import login

class OwnerPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg="white")
        
        # Top frame for store selection dropdown
        top_frame = tk.Frame(self, bg="white", bd=1, relief="solid")
        top_frame.pack(side="top", fill="x", padx=10, pady=10)
        
        tk.Label(top_frame, text="Select Store:", font=("Helvetica", 14), bg="white", fg="black").pack(side="left", padx=(10,5))
        selected_store = tk.StringVar()
        selected_store.set("Store 1")
        store_options = ["Store 1", "Store 2", "Store 3", "Store 4"]
        store_dropdown = tk.OptionMenu(top_frame, selected_store, *store_options)
        store_dropdown.config(font=("Helvetica", 14), bg="white", fg="black", relief="solid", bd=2)
        store_dropdown.pack(side="left", padx=10, pady=5)
        
        # Main frame for tabs and content
        main_frame = tk.Frame(self, bg="white")
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Left frame for tabs
        tab_frame = tk.Frame(main_frame, bg="white", width=250, bd=1, relief="solid")
        tab_frame.pack(side="left", fill="y", padx=10, pady=10)
        
        # Right frame for content
        content_frame = tk.Frame(main_frame, bg="white", bd=1, relief="solid")
        content_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        content_frame.grid_rowconfigure(0, weight=1)
        content_frame.grid_columnconfigure(0, weight=1)
        
        # Dictionary to hold tabs with forms (mirroring the ManagerPage layout)
        tabs = {}
        
        # Tab: Enter Invoice
        invoice_frame = tk.Frame(content_frame, bg="white")
        invoice_frame.grid(row=0, column=0, sticky="nsew")
        tk.Label(invoice_frame, text="Enter Invoice", font=("Helvetica", 18), bg="white", fg="black").pack(pady=10)
        tk.Label(invoice_frame, text="Invoice ID:", font=("Helvetica", 14), bg="white", fg="black").pack(pady=5)
        inv_id = tk.Entry(invoice_frame, font=("Helvetica", 14))
        inv_id.pack(pady=5)
        tk.Label(invoice_frame, text="Date:", font=("Helvetica", 14), bg="white", fg="black").pack(pady=5)
        inv_date = tk.Entry(invoice_frame, font=("Helvetica", 14))
        inv_date.pack(pady=5)
        tk.Label(invoice_frame, text="Amount:", font=("Helvetica", 14), bg="white", fg="black").pack(pady=5)
        inv_amount = tk.Entry(invoice_frame, font=("Helvetica", 14))
        inv_amount.pack(pady=5)
        tk.Button(invoice_frame, text="Submit Invoice", font=("Helvetica", 14),
                  command=lambda: messagebox.showinfo("Invoice", "Invoice Submitted")).pack(pady=10)
        tabs["Enter Invoice"] = invoice_frame
        
        # Tab: Enter Expense
        expense_frame = tk.Frame(content_frame, bg="white")
        expense_frame.grid(row=0, column=0, sticky="nsew")
        tk.Label(expense_frame, text="Enter Expense", font=("Helvetica", 18), bg="white", fg="black").pack(pady=10)
        tk.Label(expense_frame, text="Expense ID:", font=("Helvetica", 14), bg="white", fg="black").pack(pady=5)
        exp_id = tk.Entry(expense_frame, font=("Helvetica", 14))
        exp_id.pack(pady=5)
        tk.Label(expense_frame, text="Date:", font=("Helvetica", 14), bg="white", fg="black").pack(pady=5)
        exp_date = tk.Entry(expense_frame, font=("Helvetica", 14))
        exp_date.pack(pady=5)
        tk.Label(expense_frame, text="Amount:", font=("Helvetica", 14), bg="white", fg="black").pack(pady=5)
        exp_amount = tk.Entry(expense_frame, font=("Helvetica", 14))
        exp_amount.pack(pady=5)
        tk.Label(expense_frame, text="Category:", font=("Helvetica", 14), bg="white", fg="black").pack(pady=5)
        exp_category = tk.Entry(expense_frame, font=("Helvetica", 14))
        exp_category.pack(pady=5)
        tk.Button(expense_frame, text="Submit Expense", font=("Helvetica", 14),
                  command=lambda: messagebox.showinfo("Expense", "Expense Submitted")).pack(pady=10)
        tabs["Enter Expense"] = expense_frame
        
        # Tab: Enter Merchandise Sales
        sales_frame = tk.Frame(content_frame, bg="white")
        sales_frame.grid(row=0, column=0, sticky="nsew")
        tk.Label(sales_frame, text="Enter Merchandise Sales", font=("Helvetica", 18), bg="white", fg="black").pack(pady=10)
        tk.Label(sales_frame, text="Sale ID:", font=("Helvetica", 14), bg="white", fg="black").pack(pady=5)
        sale_id = tk.Entry(sales_frame, font=("Helvetica", 14))
        sale_id.pack(pady=5)
        tk.Label(sales_frame, text="Date:", font=("Helvetica", 14), bg="white", fg="black").pack(pady=5)
        sale_date = tk.Entry(sales_frame, font=("Helvetica", 14))
        sale_date.pack(pady=5)
        tk.Label(sales_frame, text="Item:", font=("Helvetica", 14), bg="white", fg="black").pack(pady=5)
        item_entry = tk.Entry(sales_frame, font=("Helvetica", 14))
        item_entry.pack(pady=5)
        tk.Label(sales_frame, text="Quantity:", font=("Helvetica", 14), bg="white", fg="black").pack(pady=5)
        qty_entry = tk.Entry(sales_frame, font=("Helvetica", 14))
        qty_entry.pack(pady=5)
        tk.Label(sales_frame, text="Price:", font=("Helvetica", 14), bg="white", fg="black").pack(pady=5)
        price_entry = tk.Entry(sales_frame, font=("Helvetica", 14))
        price_entry.pack(pady=5)
        tk.Button(sales_frame, text="Submit Sale", font=("Helvetica", 14),
                  command=lambda: messagebox.showinfo("Sales", "Sale Submitted")).pack(pady=10)
        tabs["Enter Merchandise Sales"] = sales_frame
        
        # Tab: Enter Gross Profit
        gross_frame = tk.Frame(content_frame, bg="white")
        gross_frame.grid(row=0, column=0, sticky="nsew")
        tk.Label(gross_frame, text="Enter Gross Profit", font=("Helvetica", 18), bg="white", fg="black").pack(pady=10)
        tk.Label(gross_frame, text="Total Revenue:", font=("Helvetica", 14), bg="white", fg="black").pack(pady=5)
        rev_entry = tk.Entry(gross_frame, font=("Helvetica", 14))
        rev_entry.pack(pady=5)
        tk.Label(gross_frame, text="Total Expenses:", font=("Helvetica", 14), bg="white", fg="black").pack(pady=5)
        exp_total_entry = tk.Entry(gross_frame, font=("Helvetica", 14))
        exp_total_entry.pack(pady=5)
        tk.Button(gross_frame, text="Calculate Gross Profit", font=("Helvetica", 14),
                  command=lambda: messagebox.showinfo("Gross Profit", "Gross Profit Calculated")).pack(pady=10)
        tabs["Enter Gross Profit"] = gross_frame
        
        # Tab: Withdrawal
        withdrawal_frame = tk.Frame(content_frame, bg="white")
        withdrawal_frame.grid(row=0, column=0, sticky="nsew")
        tk.Label(withdrawal_frame, text="Withdrawal", font=("Helvetica", 18), bg="white", fg="black").pack(pady=10)
        tk.Label(withdrawal_frame, text="Withdrawal ID:", font=("Helvetica", 14), bg="white", fg="black").pack(pady=5)
        with_id = tk.Entry(withdrawal_frame, font=("Helvetica", 14))
        with_id.pack(pady=5)
        tk.Label(withdrawal_frame, text="Date:", font=("Helvetica", 14), bg="white", fg="black").pack(pady=5)
        with_date = tk.Entry(withdrawal_frame, font=("Helvetica", 14))
        with_date.pack(pady=5)
        tk.Label(withdrawal_frame, text="Amount:", font=("Helvetica", 14), bg="white", fg="black").pack(pady=5)
        with_amount = tk.Entry(withdrawal_frame, font=("Helvetica", 14))
        with_amount.pack(pady=5)
        tk.Button(withdrawal_frame, text="Submit Withdrawal", font=("Helvetica", 14),
                  command=lambda: messagebox.showinfo("Withdrawal", "Withdrawal Submitted")).pack(pady=10)
        tabs["Withdrawal"] = withdrawal_frame
        
        # Tab: Calculate Employee Bonus
        bonus_frame = tk.Frame(content_frame, bg="white")
        bonus_frame.grid(row=0, column=0, sticky="nsew")
        tk.Label(bonus_frame, text="Calculate Employee Bonus", font=("Helvetica", 18), bg="white", fg="black").pack(pady=10)
        tk.Label(bonus_frame, text="Employee ID:", font=("Helvetica", 14), bg="white", fg="black").pack(pady=5)
        emp_id = tk.Entry(bonus_frame, font=("Helvetica", 14))
        emp_id.pack(pady=5)
        tk.Label(bonus_frame, text="Sales Amount:", font=("Helvetica", 14), bg="white", fg="black").pack(pady=5)
        sales_amt = tk.Entry(bonus_frame, font=("Helvetica", 14))
        sales_amt.pack(pady=5)
        tk.Label(bonus_frame, text="Bonus Percentage:", font=("Helvetica", 14), bg="white", fg="black").pack(pady=5)
        bonus_pct = tk.Entry(bonus_frame, font=("Helvetica", 14))
        bonus_pct.pack(pady=5)
        
        def calculate_bonus():
            try:
                sales = float(sales_amt.get())
                percent = float(bonus_pct.get())
                bonus = sales * percent / 100
                messagebox.showinfo("Bonus", f"Calculated Bonus: {bonus:.2f}")
            except ValueError:
                messagebox.showerror("Error", "Please enter valid numbers")
                
        tk.Button(bonus_frame, text="Calculate Bonus", font=("Helvetica", 14),
                  command=calculate_bonus).pack(pady=10)
        tabs["Calculate Employee Bonus"] = bonus_frame
        
        # Tab: Add Employee
        add_emp_frame = tk.Frame(content_frame, bg="white")
        add_emp_frame.grid(row=0, column=0, sticky="nsew")
        tk.Label(add_emp_frame, text="Add Employee", font=("Helvetica", 18), bg="white", fg="black").pack(pady=10)
        tk.Label(add_emp_frame, text="Employee Name:", font=("Helvetica", 14), bg="white", fg="black").pack(pady=5)
        emp_name = tk.Entry(add_emp_frame, font=("Helvetica", 14))
        emp_name.pack(pady=5)
        tk.Label(add_emp_frame, text="Role:", font=("Helvetica", 14), bg="white", fg="black").pack(pady=5)
        role_var = tk.StringVar(add_emp_frame)
        role_var.set("employee")
        role_menu = tk.OptionMenu(add_emp_frame, role_var, "employee", "manager", "owner")
        role_menu.config(font=("Helvetica", 14), bg="white", fg="black")
        role_menu.pack(pady=5)
        tk.Button(add_emp_frame, text="Add Employee", font=("Helvetica", 14),
                  command=lambda: messagebox.showinfo("Add Employee", "Employee Added")).pack(pady=10)
        tabs["Add Employee"] = add_emp_frame
        
        def show_tab(tab_name):
            tabs[tab_name].tkraise()
        
        for title in tabs:
            btn = tk.Button(tab_frame, text=title, font=("Helvetica", 14), fg="black", bg="white",
                            relief="flat", bd=2, command=lambda t=title: show_tab(t), width=25, height=3)
            btn.pack(pady=5, padx=10, fill="x")
        
        logout_button = tk.Button(tab_frame, text="Logout", font=("Helvetica", 14), fg="black", bg="white",
                                  relief="flat", bd=2, command=lambda: controller.show_frame("LoginPage"),
                                  width=25, height=3)
        logout_button.pack(side="bottom", pady=10, padx=10)
        
        show_tab("Enter Invoice")

if __name__ == '__main__':
    root = tk.Tk()
    root.title("Owner Dashboard")
    root.geometry("900x750")
    owner_page = OwnerPage(root, None)
    owner_page.pack(fill="both", expand=True)
    root.mainloop()
