import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime, timedelta
import sqlConnector


class ManageEmployees(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg="white")

        # Initialize weekly start dates for Expenses, Merchandise, Gross Profit History (set to Monday)
        self.current_week_start = datetime.now().date() - timedelta(days=datetime.now().date().weekday())
        self.current_merch_week_start = datetime.now().date() - timedelta(days=datetime.now().date().weekday())
        self.current_profit_week_start = datetime.now().date() - timedelta(days=datetime.now().date().weekday())
        # For Payroll, initialize with the most recent Sunday
        self.current_payroll_sunday = self.get_most_recent_sunday(datetime.now().date())
        # For Employee History, initialize current date (daily)
        self.current_date = datetime.now().date()
        self.create_bottom_frame()
        # Top frame for store selection dropdown
        top_frame = tk.Frame(self, bg="white", bd=1, relief="solid")
        top_frame.pack(side="top", fill="x", padx=10, pady=10)

        # Centered label (ALOHA)
        aloha_label = tk.Label(top_frame, text="ALOHA", font=("Helvetica", 14), bg="white", fg="black")
        aloha_label.place(relx=0.5, rely=0.5, anchor="center")

        # Right label (name of employee)
        tk.Label(top_frame, text="Name of employee", font=("Helvetica", 14), bg="white", fg="black").pack(side="right",
                                                                                                          padx=(5, 10))

        selected_store = tk.StringVar()
        selected_store.set("Store 1")
        store_options = ["Store 1", "Store 2", "Store 3", "Store 4"]
        store_dropdown = tk.OptionMenu(top_frame, selected_store, *store_options)
        store_dropdown.config(font=("Helvetica", 14), bg="white", fg="black", relief="solid", bd=2)
        store_dropdown.pack(side="left", padx=10, pady=5)

        # Create Main Layout
        main_frame = tk.Frame(self, bg="white")
        main_frame.pack(fill="both", expand=True)

        # Left Panel for Tabs
        tab_frame = tk.Frame(main_frame, bg="white", width=250, bd=1, relief="solid")
        tab_frame.pack(side="left", fill="y", padx=10, pady=10)
        
        # Right Panel for Content
        content_frame = tk.Frame(main_frame, bg="white", bd=1, relief="solid")
        content_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        content_frame.grid_rowconfigure(0, weight=1)
        content_frame.grid_columnconfigure(0, weight=1)

        # Dictionary to hold the tabs
        tabs = {}

        # -------------------------------
        # Enter Invoice Tab (as provided)
        # -------------------------------
        enter_invoice_frame = tk.Frame(content_frame, bg="white")
        enter_invoice_frame.grid(row=0, column=0, sticky="nsew")
        tk.Label(enter_invoice_frame, text="Enter Invoice", font=("Helvetica", 18), bg="white").pack(pady=10)
        
        tk.Label(enter_invoice_frame, text="Invoice ID:", font=("Helvetica", 14), bg="white").pack()
        invoice_id = tk.Entry(enter_invoice_frame, font=("Helvetica", 14))
        invoice_id.pack()
        
        tk.Label(enter_invoice_frame, text="Date:", font=("Helvetica", 14), bg="white").pack()
        invoice_date = tk.Entry(enter_invoice_frame, font=("Helvetica", 14))
        invoice_date.pack()
        
        tk.Label(enter_invoice_frame, text="Company:", font=("Helvetica", 14), bg="white").pack()
        invoice_company = tk.Entry(enter_invoice_frame, font=("Helvetica", 14))
        invoice_company.pack()
        
        tk.Label(enter_invoice_frame, text="Paid (Yes/No):", font=("Helvetica", 14), bg="white").pack()
        invoice_paid = tk.Entry(enter_invoice_frame, font=("Helvetica", 14))
        invoice_paid.pack()
        
        tk.Label(enter_invoice_frame, text="Amount:", font=("Helvetica", 14), bg="white").pack()
        invoice_amount = tk.Entry(enter_invoice_frame, font=("Helvetica", 14))
        invoice_amount.pack()
        
        tk.Label(enter_invoice_frame, text="Amount Paid:", font=("Helvetica", 14), bg="white").pack()
        amount_paid = tk.Entry(enter_invoice_frame, font=("Helvetica", 14))
        amount_paid.pack()
        
        tk.Button(enter_invoice_frame, text="Submit Invoice", font=("Helvetica", 14), 
                  command=lambda: self.submit_invoice(invoice_id.get(), invoice_date.get(), invoice_company.get(), 
                                                      invoice_paid.get(), invoice_amount.get(), amount_paid.get())).pack(pady=10)
        
        tabs["Enter Invoice"] = enter_invoice_frame

        # -------------------------------
        # Enter Expense Tab
        # -------------------------------
        enter_expense_frame = tk.Frame(content_frame, bg="white")
        enter_expense_frame.grid(row=0, column=0, sticky="nsew")
        tk.Label(enter_expense_frame, text="Enter Expense", font=("Helvetica", 18), bg="white").pack(pady=10)
        
        tk.Label(enter_expense_frame, text="Expense Type:", font=("Helvetica", 14), bg="white").pack()
        expense_type = tk.Entry(enter_expense_frame, font=("Helvetica", 14))
        expense_type.pack()
        
        tk.Label(enter_expense_frame, text="Expense Value:", font=("Helvetica", 14), bg="white").pack()
        expense_value = tk.Entry(enter_expense_frame, font=("Helvetica", 14))
        expense_value.pack()
        
        tk.Label(enter_expense_frame, text="Expense Date:", font=("Helvetica", 14), bg="white").pack()
        expense_date = tk.Entry(enter_expense_frame, font=("Helvetica", 14))
        expense_date.pack()
        
        tk.Button(enter_expense_frame, text="Submit Expense", font=("Helvetica", 14),
                  command=lambda: self.submit_expense(expense_type.get(), expense_value.get(), expense_date.get())).pack(pady=10)
        
        tabs["Enter Expense"] = enter_expense_frame

        # -------------------------------
        # Enter Merchandise Tab
        # -------------------------------
        enter_merch_frame = tk.Frame(content_frame, bg="white")
        enter_merch_frame.grid(row=0, column=0, sticky="nsew")
        tk.Label(enter_merch_frame, text="Enter Merchandise", font=("Helvetica", 18), bg="white").pack(pady=10)
        
        tk.Label(enter_merch_frame, text="Merchandise Type:", font=("Helvetica", 14), bg="white").pack()
        merch_type = tk.Entry(enter_merch_frame, font=("Helvetica", 14))
        merch_type.pack()
        
        tk.Label(enter_merch_frame, text="Merchandise Value:", font=("Helvetica", 14), bg="white").pack()
        merch_value = tk.Entry(enter_merch_frame, font=("Helvetica", 14))
        merch_value.pack()
        
        tk.Label(enter_merch_frame, text="Merchandise Date:", font=("Helvetica", 14), bg="white").pack()
        merch_date = tk.Entry(enter_merch_frame, font=("Helvetica", 14))
        merch_date.pack()
        
        tk.Button(enter_merch_frame, text="Submit Merchandise", font=("Helvetica", 14),
                  command=lambda: self.submit_merchandise(merch_type.get(), merch_value.get(), merch_date.get())).pack(pady=10)
        
        tabs["Enter Merchandise"] = enter_merch_frame

        # -------------------------------
        # Employee History Tab (Daily)
        # -------------------------------
        employee_history_frame = tk.Frame(content_frame, bg="white")
        employee_history_frame.grid(row=0, column=0, sticky="nsew")
        tabs["Employee History"] = employee_history_frame

        tk.Label(employee_history_frame, text="Employee History", font=("Helvetica", 18), bg="white").pack(pady=10)

        nav_frame = tk.Frame(employee_history_frame, bg="white")
        nav_frame.pack(pady=10)
        prev_button = tk.Button(nav_frame, text="<", font=("Helvetica", 14), command=self.previous_day)
        prev_button.pack(side="left", padx=5)
        self.date_label = tk.Label(nav_frame, text=self.current_date.strftime("%Y-%m-%d"), font=("Helvetica", 14), bg="white")
        self.date_label.pack(side="left", padx=5)
        next_button = tk.Button(nav_frame, text=">", font=("Helvetica", 14), command=self.next_day)
        next_button.pack(side="left", padx=5)

        tk.Label(employee_history_frame, text="Enter Date (YYYY-MM-DD):", font=("Helvetica", 14), bg="white").pack(pady=(20,5))
        self.date_entry = tk.Entry(employee_history_frame, font=("Helvetica", 14))
        self.date_entry.pack(pady=5)
        tk.Button(employee_history_frame, text="Go", font=("Helvetica", 14), command=self.set_date_from_entry).pack(pady=5)

        self.history_placeholder = tk.Label(employee_history_frame, text="", font=("Helvetica", 12), bg="white")
        self.history_placeholder.pack(pady=20)
        self.update_history_display()

        # -------------------------------
        # Expenses History Tab (Weekly)
        # -------------------------------
        expenses_history_frame = tk.Frame(content_frame, bg="white")
        expenses_history_frame.grid(row=0, column=0, sticky="nsew")
        tabs["Expenses History"] = expenses_history_frame

        tk.Label(expenses_history_frame, text="Expenses History", font=("Helvetica", 18), bg="white").pack(pady=10)

        exp_nav_frame = tk.Frame(expenses_history_frame, bg="white")
        exp_nav_frame.pack(pady=10)
        prev_week_btn = tk.Button(exp_nav_frame, text="<", font=("Helvetica", 14), command=self.previous_week)
        prev_week_btn.pack(side="left", padx=5)
        self.week_label = tk.Label(exp_nav_frame, text="", font=("Helvetica", 14), bg="white")
        self.week_label.pack(side="left", padx=5)
        next_week_btn = tk.Button(exp_nav_frame, text=">", font=("Helvetica", 14), command=self.next_week)
        next_week_btn.pack(side="left", padx=5)

        tk.Label(expenses_history_frame, text="Enter Date (YYYY-MM-DD):", font=("Helvetica", 14), bg="white").pack(pady=(20,5))
        self.week_entry = tk.Entry(expenses_history_frame, font=("Helvetica", 14))
        self.week_entry.pack(pady=5)
        tk.Button(expenses_history_frame, text="Go", font=("Helvetica", 14), command=self.set_week_from_entry).pack(pady=5)

        self.expenses_history_placeholder = tk.Label(expenses_history_frame, text="", font=("Helvetica", 12), bg="white")
        self.expenses_history_placeholder.pack(pady=20)
        self.update_expenses_history_display()

        # -------------------------------
        # Merchandise History Tab (Weekly)
        # -------------------------------
        merch_history_frame = tk.Frame(content_frame, bg="white")
        merch_history_frame.grid(row=0, column=0, sticky="nsew")
        tabs["Merchandise History"] = merch_history_frame

        tk.Label(merch_history_frame, text="Merchandise History", font=("Helvetica", 18), bg="white").pack(pady=10)

        merch_nav_frame = tk.Frame(merch_history_frame, bg="white")
        merch_nav_frame.pack(pady=10)
        prev_merch_btn = tk.Button(merch_nav_frame, text="<", font=("Helvetica", 14), command=self.previous_merch_week)
        prev_merch_btn.pack(side="left", padx=5)
        self.merch_week_label = tk.Label(merch_nav_frame, text="", font=("Helvetica", 14), bg="white")
        self.merch_week_label.pack(side="left", padx=5)
        next_merch_btn = tk.Button(merch_nav_frame, text=">", font=("Helvetica", 14), command=self.next_merch_week)
        next_merch_btn.pack(side="left", padx=5)

        tk.Label(merch_history_frame, text="Enter Date (YYYY-MM-DD):", font=("Helvetica", 14), bg="white").pack(pady=(20,5))
        self.merch_week_entry = tk.Entry(merch_history_frame, font=("Helvetica", 14))
        self.merch_week_entry.pack(pady=5)
        tk.Button(merch_history_frame, text="Go", font=("Helvetica", 14), command=self.set_merch_week_from_entry).pack(pady=5)

        self.merch_history_placeholder = tk.Label(merch_history_frame, text="", font=("Helvetica", 12), bg="white")
        self.merch_history_placeholder.pack(pady=20)
        self.update_merch_history_display()

        # -------------------------------
        # Gross Profit Tab (Weekly)
        # -------------------------------
        gross_profit_frame = tk.Frame(content_frame, bg="white")
        gross_profit_frame.grid(row=0, column=0, sticky="nsew")
        tabs["Gross Profit"] = gross_profit_frame

        tk.Label(gross_profit_frame, text="Gross Profit", font=("Helvetica", 18), bg="white").pack(pady=10)

        profit_nav_frame = tk.Frame(gross_profit_frame, bg="white")
        profit_nav_frame.pack(pady=10)
        prev_profit_btn = tk.Button(profit_nav_frame, text="<", font=("Helvetica", 14), command=self.previous_profit_week)
        prev_profit_btn.pack(side="left", padx=5)
        self.profit_week_label = tk.Label(profit_nav_frame, text="", font=("Helvetica", 14), bg="white")
        self.profit_week_label.pack(side="left", padx=5)
        next_profit_btn = tk.Button(profit_nav_frame, text=">", font=("Helvetica", 14), command=self.next_profit_week)
        next_profit_btn.pack(side="left", padx=5)

        tk.Label(gross_profit_frame, text="Enter Date (YYYY-MM-DD):", font=("Helvetica", 14), bg="white").pack(pady=(20,5))
        self.profit_week_entry = tk.Entry(gross_profit_frame, font=("Helvetica", 14))
        self.profit_week_entry.pack(pady=5)
        tk.Button(gross_profit_frame, text="Go", font=("Helvetica", 14), command=self.set_profit_week_from_entry).pack(pady=5)

        # Create a Treeview for the gross profit table
        self.gross_profit_tree = ttk.Treeview(gross_profit_frame, columns=("Date", "Cash", "Credit", "Total"), show="headings")
        self.gross_profit_tree.heading("Date", text="Date")
        self.gross_profit_tree.heading("Cash", text="Cash")
        self.gross_profit_tree.heading("Credit", text="Credit")
        self.gross_profit_tree.heading("Total", text="Total")
        self.gross_profit_tree.pack(fill="both", expand=True, padx=10, pady=10)
        self.update_gross_profit_display()

        # -------------------------------
        # Payroll Tab
        # -------------------------------
        payroll_frame = tk.Frame(content_frame, bg="white")
        payroll_frame.grid(row=0, column=0, sticky="nsew")
        tabs["Payroll"] = payroll_frame

        tk.Label(payroll_frame, text="Payroll", font=("Helvetica", 18), bg="white").pack(pady=10)

        # Employee selection dropdown
        tk.Label(payroll_frame, text="Select Employee:", font=("Helvetica", 14), bg="white").pack(pady=(10,5))
        self.payroll_employee_var = tk.StringVar()
        self.payroll_employee_var.set("Alice")
        employees = ["Alice", "Bob", "Charlie", "David"]
        payroll_dropdown = tk.OptionMenu(payroll_frame, self.payroll_employee_var, *employees)
        payroll_dropdown.config(font=("Helvetica", 14), bg="white")
        payroll_dropdown.pack(pady=5)

        # Payroll navigation
        payroll_nav_frame = tk.Frame(payroll_frame, bg="white")
        payroll_nav_frame.pack(pady=10)
        payroll_prev_btn = tk.Button(payroll_nav_frame, text="<", font=("Helvetica", 14), command=self.previous_payroll_week)
        payroll_prev_btn.pack(side="left", padx=5)
        self.payroll_date_label = tk.Label(payroll_nav_frame, text=self.current_payroll_sunday.strftime("%Y-%m-%d"), font=("Helvetica", 14), bg="white")
        self.payroll_date_label.pack(side="left", padx=5)
        payroll_next_btn = tk.Button(payroll_nav_frame, text=">", font=("Helvetica", 14), command=self.next_payroll_week)
        payroll_next_btn.pack(side="left", padx=5)

        tk.Label(payroll_frame, text="Enter Date (YYYY-MM-DD):", font=("Helvetica", 14), bg="white").pack(pady=(20,5))
        self.payroll_date_entry = tk.Entry(payroll_frame, font=("Helvetica", 14))
        self.payroll_date_entry.pack(pady=5)
        tk.Button(payroll_frame, text="Go", font=("Helvetica", 14), command=self.set_payroll_date_from_entry).pack(pady=5)

        # Payroll table showing previous 4 Sundays and pay (placeholder)
        self.payroll_tree = ttk.Treeview(payroll_frame, columns=("Date", "Pay"), show="headings")
        self.payroll_tree.heading("Date", text="Date")
        self.payroll_tree.heading("Pay", text="Pay")
        self.payroll_tree.pack(fill="both", expand=True, padx=10, pady=10)
        self.update_payroll_display()

        # -------------------------------
        # Manage Employees Tab (Notebook)
        # -------------------------------
        manage_frame = tk.Frame(content_frame, bg="white")
        manage_frame.grid(row=0, column=0, sticky="nsew")
        notebook = ttk.Notebook(manage_frame)
        notebook.pack(expand=True, fill="both")
        # Add Employee Tab
        add_employee_frame = tk.Frame(notebook, bg="white")
        tk.Label(add_employee_frame, text="Add Employee", font=("Helvetica", 18), bg="white").pack(pady=10)


        tk.Label(add_employee_frame, text="First Name", font=("Helvetica", 14), bg="white").pack()
        emp_firstname = tk.Entry(add_employee_frame, font=("Helvetica", 14))
        emp_firstname.pack()

        tk.Label(add_employee_frame, text="Last Name:", font=("Helvetica", 14), bg="white").pack()
        emp_lastname = tk.Entry(add_employee_frame, font=("Helvetica", 14))
        emp_lastname.pack()
        tk.Label(add_employee_frame, text="Username:", font=("Helvetica", 14), bg="white").pack()
        emp_username = tk.Entry(add_employee_frame, font=("Helvetica", 14))
        emp_username.pack()
        tk.Label(add_employee_frame, text="Password:", font=("Helvetica", 14), bg="white").pack()
        emp_password = tk.Entry(add_employee_frame, font=("Helvetica", 14), show="*")
        emp_password.pack()

        # Role Dropdown Menu
        tk.Label(add_employee_frame, text="Role:", font=("Helvetica", 14), bg="white").pack()
        roles = ["Employee", "Manager","Owner"]  # List of roles
        selected_role = tk.StringVar()
        selected_role.set(roles[0])  # Set default role
        role_menu = tk.OptionMenu(add_employee_frame, selected_role, *roles)
        role_menu.config(font=("Helvetica", 14))
        role_menu.pack()

        tk.Button(add_employee_frame, text="Add Employee", font=("Helvetica", 14),
                  command=lambda: self.add_employee(emp_firstname.get(), emp_lastname.get(), emp_username.get(), emp_password.get(),
                                                 selected_role.get())).pack(pady=10)

        # Delete Employee Tab
        delete_employee_frame = tk.Frame(notebook, bg="white")
        tk.Label(delete_employee_frame, text="Delete Employee", font=("Helvetica", 18), bg="white").pack(pady=10)
        tk.Label(delete_employee_frame, text="Username:", font=("Helvetica", 14), bg="white").pack()
        del_username = tk.Entry(delete_employee_frame, font=("Helvetica", 14))
        del_username.pack()
        tk.Button(delete_employee_frame, text="Delete", font=("Helvetica", 14), 
                  command=lambda: self.delete_employee(del_username.get())).pack(pady=10)

        # Edit Employee Tab
        edit_employee_frame = tk.Frame(notebook, bg="white")
        tk.Label(edit_employee_frame, text="Edit Employee", font=("Helvetica", 18), bg="white").pack(pady=10)
        tk.Label(edit_employee_frame, text="Username:", font=("Helvetica", 14), bg="white").pack()
        edit_username = tk.Entry(edit_employee_frame, font=("Helvetica", 14))
        edit_username.pack()
        tk.Label(edit_employee_frame, text="New Password:", font=("Helvetica", 14), bg="white").pack()
        new_password = tk.Entry(edit_employee_frame, font=("Helvetica", 14), show="*")
        new_password.pack()
        tk.Label(edit_employee_frame, text="Edit Bonus Percentage:", font=("Helvetica", 14), bg="white").pack()
        new_bonus = tk.Entry(edit_employee_frame, font=("Helvetica", 14))
        new_bonus.pack()
        tk.Button(edit_employee_frame, text="Update", font=("Helvetica", 14),
                  command=lambda: self.edit_employee(edit_username.get(), new_password.get(), new_bonus.get())).pack(pady=10)

        notebook.add(add_employee_frame, text="Add Employee")
        notebook.add(delete_employee_frame, text="Delete Employee")
        notebook.add(edit_employee_frame, text="Edit Employee")
        
        tabs["Manage Employees"] = manage_frame


        # -------------------------------
        # Function to Show Selected Tab
        # -------------------------------
        def show_tab(tab_name):
            tabs[tab_name].tkraise()
        
        for title in tabs:
            btn = tk.Button(tab_frame, text=title, font=("Helvetica", 14), fg="black", bg="white",
                            relief="solid", bd=2, command=lambda t=title: show_tab(t), width=25, height=2)
            btn.pack(pady=5, padx=10, fill="x")
        
        # Show the default tab
        show_tab("Enter Invoice")
    
    # -------------------------------
    # Placeholder Methods
    # -------------------------------

    def create_bottom_frame(self):
        """Creates a bottom frame for the logout button."""
        bottom_frame = tk.Frame(self, bg="white", bd=1, relief="solid")
        bottom_frame.pack(side="bottom", fill="x", padx=10, pady=10)

        logout_button = tk.Button(bottom_frame, text="Logout", font=("Helvetica", 14), bg="red", fg="white",
                                  command=self.logout)
        logout_button.pack(side="left", padx=10, pady=5)

    def logout(self):
        """Handles logout and returns to the login page."""
        confirm = messagebox.askyesno("Logout", "Are you sure you want to logout?")
        if confirm:
            self.controller.show_frame("LoginPage")
    def submit_invoice(self, invoice_id, invoice_date, invoice_company, invoice_paid, invoice_amount, amount_paid):
        messagebox.showinfo("Submit Invoice", f"Invoice {invoice_id} submitted!")
    
    def submit_expense(self, expense_type, expense_value, expense_date):
        messagebox.showinfo("Submit Expense", f"Expense '{expense_type}' submitted!")
    
    def submit_merchandise(self, merch_type, merch_value, merch_date):
        messagebox.showinfo("Submit Merchandise", f"Merchandise '{merch_type}' submitted!")
    
    def add_employee(self, firstName, lastName, username, password, selectedRole):
        if not firstName or not lastName or not password or not selectedRole:
            messagebox.showerror("Error", "All fields must be filled out.")
            return
        messagebox.showinfo("Success", f"Employee {firstName} {lastName} added successfully!")
        # sends info to database
        query = """INSERT INTO employee(firstName,lastName, username, password,role)
           VALUES (%s, %s, %s, %s,%s)"""
        data = (firstName, lastName, username,password,selectedRole)

        # send data to sql connector
        sqlConnector.connect(query, data)

    def delete_employee(self, username):
        if not username:
            messagebox.showerror("Error", "Username is required.")
            return
        messagebox.showinfo("Success", f"Employee {username} deleted successfully!")
    
    def edit_employee(self, username, password, bonus):
        if not username:
            messagebox.showerror("Error", "Username is required.")
            return
        messagebox.showinfo("Success", f"Employee {username} updated successfully!")
    
    # -------------------------------
    # Employee History (Daily) Methods
    # -------------------------------
    def update_history_display(self):
        self.history_placeholder.config(text=f"No clock-in records for {self.current_date.strftime('%Y-%m-%d')}.")
    
    def previous_day(self):
        self.current_date -= timedelta(days=1)
        self.date_label.config(text=self.current_date.strftime("%Y-%m-%d"))
        self.update_history_display()
    
    def next_day(self):
        self.current_date += timedelta(days=1)
        self.date_label.config(text=self.current_date.strftime("%Y-%m-%d"))
        self.update_history_display()
    
    def set_date_from_entry(self):
        try:
            new_date = datetime.strptime(self.date_entry.get(), "%Y-%m-%d").date()
            self.current_date = new_date
            self.date_label.config(text=self.current_date.strftime("%Y-%m-%d"))
            self.update_history_display()
        except ValueError:
            messagebox.showerror("Invalid Date", "Please enter a valid date in YYYY-MM-DD format.")
    
    # -------------------------------
    # Expenses History (Weekly) Methods
    # -------------------------------
    def update_expenses_history_display(self):
        week_end = self.current_week_start + timedelta(days=6)
        self.week_label.config(text=f"{self.current_week_start.strftime('%Y-%m-%d')} to {week_end.strftime('%Y-%m-%d')}")
        self.expenses_history_placeholder.config(
            text=f"No expenses recorded for the week of {self.current_week_start.strftime('%Y-%m-%d')} to {week_end.strftime('%Y-%m-%d')}.")
    
    def previous_week(self):
        self.current_week_start -= timedelta(weeks=1)
        self.update_expenses_history_display()
    
    def next_week(self):
        self.current_week_start += timedelta(weeks=1)
        self.update_expenses_history_display()
    
    def set_week_from_entry(self):
        try:
            new_date = datetime.strptime(self.week_entry.get(), "%Y-%m-%d").date()
            self.current_week_start = new_date - timedelta(days=new_date.weekday())
            self.update_expenses_history_display()
        except ValueError:
            messagebox.showerror("Invalid Date", "Please enter a valid date in YYYY-MM-DD format.")
    
    # -------------------------------
    # Merchandise History (Weekly) Methods
    # -------------------------------
    def update_merch_history_display(self):
        merch_week_end = self.current_merch_week_start + timedelta(days=6)
        self.merch_week_label.config(text=f"{self.current_merch_week_start.strftime('%Y-%m-%d')} to {merch_week_end.strftime('%Y-%m-%d')}")
        self.merch_history_placeholder.config(
            text=f"No merchandise recorded for the week of {self.current_merch_week_start.strftime('%Y-%m-%d')} to {merch_week_end.strftime('%Y-%m-%d')}.")
    
    def previous_merch_week(self):
        self.current_merch_week_start -= timedelta(weeks=1)
        self.update_merch_history_display()
    
    def next_merch_week(self):
        self.current_merch_week_start += timedelta(weeks=1)
        self.update_merch_history_display()
    
    def set_merch_week_from_entry(self):
        try:
            new_date = datetime.strptime(self.merch_week_entry.get(), "%Y-%m-%d").date()
            self.current_merch_week_start = new_date - timedelta(days=new_date.weekday())
            self.update_merch_history_display()
        except ValueError:
            messagebox.showerror("Invalid Date", "Please enter a valid date in YYYY-MM-DD format.")
    
    # -------------------------------
    # Gross Profit (Weekly) Methods
    # -------------------------------
    def update_gross_profit_display(self):
        profit_week_end = self.current_profit_week_start + timedelta(days=6)
        self.profit_week_label.config(text=f"{self.current_profit_week_start.strftime('%Y-%m-%d')} to {profit_week_end.strftime('%Y-%m-%d')}")
        # Clear the treeview
        for row in self.gross_profit_tree.get_children():
            self.gross_profit_tree.delete(row)
        # Insert a dummy row for each day of the week (placeholders)
        for i in range(7):
            day = self.current_profit_week_start + timedelta(days=i)
            self.gross_profit_tree.insert("", "end", values=(day.strftime("%Y-%m-%d"), "0", "0", "0"))
    
    def previous_profit_week(self):
        self.current_profit_week_start -= timedelta(weeks=1)
        self.update_gross_profit_display()
    
    def next_profit_week(self):
        self.current_profit_week_start += timedelta(weeks=1)
        self.update_gross_profit_display()
    
    def set_profit_week_from_entry(self):
        try:
            new_date = datetime.strptime(self.profit_week_entry.get(), "%Y-%m-%d").date()
            self.current_profit_week_start = new_date - timedelta(days=new_date.weekday())
            self.update_gross_profit_display()
        except ValueError:
            messagebox.showerror("Invalid Date", "Please enter a valid date in YYYY-MM-DD format.")
    
    # -------------------------------
    # Payroll Methods
    # -------------------------------
    def get_most_recent_sunday(self, d):
        # Python's weekday(): Monday is 0 ... Sunday is 6
        days_since_sunday = (d.weekday() + 1) % 7
        return d - timedelta(days=days_since_sunday)
    
    def update_payroll_display(self):
        # Clear the treeview
        for row in self.payroll_tree.get_children():
            self.payroll_tree.delete(row)
        # Insert rows for the previous 4 Sundays (including current)
        for i in range(4):
            sunday_date = self.current_payroll_sunday - timedelta(weeks=i)
            self.payroll_tree.insert("", "end", values=(sunday_date.strftime("%Y-%m-%d"), "0"))
    
    def previous_payroll_week(self):
        self.current_payroll_sunday -= timedelta(weeks=1)
        self.payroll_date_label.config(text=self.current_payroll_sunday.strftime("%Y-%m-%d"))
        self.update_payroll_display()
    
    def next_payroll_week(self):
        self.current_payroll_sunday += timedelta(weeks=1)
        self.payroll_date_label.config(text=self.current_payroll_sunday.strftime("%Y-%m-%d"))
        self.update_payroll_display()
    
    def set_payroll_date_from_entry(self):
        try:
            new_date = datetime.strptime(self.payroll_date_entry.get(), "%Y-%m-%d").date()
            self.current_payroll_sunday = self.get_most_recent_sunday(new_date)
            self.payroll_date_label.config(text=self.current_payroll_sunday.strftime("%Y-%m-%d"))
            self.update_payroll_display()
        except ValueError:
            messagebox.showerror("Invalid Date", "Please enter a valid date in YYYY-MM-DD format.")




# For testing purposes, run this file directly.
if __name__ == '__main__':
    root = tk.Tk()
    root.title("EMS Application - Manage Employees")
    root.geometry("900x750")
    app = ManageEmployees(root, None)
    app.pack(fill="both", expand=True)
    root.mainloop()
