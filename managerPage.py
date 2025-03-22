import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime, timedelta
import sqlConnector  # Assuming this is your custom module for database connections


class ManageEmployees(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg="white")  # Set background color for the frame

        # Initialize weekly start dates for Expenses, Merchandise, Gross Profit History (set to Monday)
        self.current_week_start = datetime.now().date() - timedelta(days=datetime.now().date().weekday())
        self.current_merch_week_start = datetime.now().date() - timedelta(days=datetime.now().date().weekday())
        self.current_profit_week_start = datetime.now().date() - timedelta(days=datetime.now().date().weekday())

        # For Payroll, initialize with the most recent Sunday
        self.current_payroll_sunday = self.get_most_recent_sunday(datetime.now().date())

        # For Employee History, initialize current date (daily)
        self.current_date = datetime.now().date()

        # Create the bottom frame (for logout button)
        self.create_bottom_frame()

        # -------------------------------
        # Top Frame (Store Selection and Employee Name)
        # -------------------------------
        top_frame = tk.Frame(self, bg="white", bd=1, relief="solid")
        top_frame.pack(side="top", fill="x", padx=10, pady=10)

        # Centered label (ALOHA)
        aloha_label = tk.Label(top_frame, text="ALOHA", font=("Helvetica", 14), bg="white", fg="black")
        aloha_label.place(relx=0.5, rely=0.5, anchor="center")

        # Right label (name of employee)
        tk.Label(top_frame, text="Name of employee", font=("Helvetica", 14), bg="white", fg="black").pack(side="right",
                                                                                                          padx=(5, 10))

        # Store selection dropdown
        selected_store = tk.StringVar()
        selected_store.set("Store 1")  # Default store
        store_options = ["Store 1", "Store 2", "Store 3", "Store 4"]
        store_dropdown = tk.OptionMenu(top_frame, selected_store, *store_options)
        store_dropdown.config(font=("Helvetica", 14), bg="white", fg="black", relief="solid", bd=2)
        store_dropdown.pack(side="left", padx=10, pady=5)

        # -------------------------------
        # Main Layout (Left Tabs and Right Content)
        # -------------------------------
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
        # Enter Invoice Tab
        # -------------------------------
        enter_invoice_frame = tk.Frame(content_frame, bg="white")
        enter_invoice_frame.grid(row=0, column=0, sticky="nsew")
        tk.Label(enter_invoice_frame, text="Enter Invoice", font=("Helvetica", 18), bg="white").pack(pady=10)

        # Invoice fields
        fields = ["Invoice ID:", "Date:", "Company:", "Paid (Yes/No):", "Amount:", "Amount Paid:"]
        entries = []
        for field in fields:
            tk.Label(enter_invoice_frame, text=field, font=("Helvetica", 14), bg="white").pack()
            entry = tk.Entry(enter_invoice_frame, font=("Helvetica", 14))
            entry.pack()
            entries.append(entry)

        # Submit button
        tk.Button(enter_invoice_frame, text="Submit Invoice", font=("Helvetica", 14),
                  command=lambda: self.submit_invoice(*[entry.get() for entry in entries])).pack(pady=10)

        tabs["Enter Invoice"] = enter_invoice_frame

        # -------------------------------
        # Employee History Tab (Daily)
        # -------------------------------
        employee_history_frame = tk.Frame(content_frame, bg="white")
        employee_history_frame.grid(row=0, column=0, sticky="nsew")
        tabs["Employee History"] = employee_history_frame

        tk.Label(employee_history_frame, text="Employee History", font=("Helvetica", 18), bg="white").pack(pady=10)

        # Navigation Frame for Date Control
        nav_frame = tk.Frame(employee_history_frame, bg="white")
        nav_frame.pack(pady=10)
        prev_button = tk.Button(nav_frame, text="<", font=("Helvetica", 14), command=self.previous_day)
        prev_button.pack(side="left", padx=5)
        self.date_label = tk.Label(nav_frame, text=self.current_date.strftime("%Y-%m-%d"), font=("Helvetica", 14), bg="white")
        self.date_label.pack(side="left", padx=5)
        next_button = tk.Button(nav_frame, text=">", font=("Helvetica", 14), command=self.next_day)
        next_button.pack(side="left", padx=5)

        # Date Entry for Manual Date Selection
        tk.Label(employee_history_frame, text="Enter Date (YYYY-MM-DD):", font=("Helvetica", 14), bg="white").pack(pady=(20,5))
        self.date_entry = tk.Entry(employee_history_frame, font=("Helvetica", 14))
        self.date_entry.pack(pady=5)
        tk.Button(employee_history_frame, text="Go", font=("Helvetica", 14), command=self.set_date_from_entry).pack(pady=5)

        # Table to Display Employee History
        columns = ("Employee", "Clock-In", "Clock-Out", "Hours Worked")
        self.history_tree = ttk.Treeview(employee_history_frame, columns=columns, show="headings")
        for col in columns:
            self.history_tree.heading(col, text=col)
        self.history_tree.pack(fill="both", expand=True, padx=10, pady=10)

        # Placeholder for No Records
        self.history_placeholder = tk.Label(employee_history_frame, text="", font=("Helvetica", 12), bg="white")
        self.history_placeholder.pack(pady=20)

        # Update the Display
        self.update_history_display()

        # -------------------------------
        # Expenses History Tab (Weekly)
        # -------------------------------
        expenses_history_frame = tk.Frame(content_frame, bg="white")
        expenses_history_frame.grid(row=0, column=0, sticky="nsew")
        tabs["Expenses History"] = expenses_history_frame

        tk.Label(expenses_history_frame, text="Expenses History", font=("Helvetica", 18), bg="white").pack(pady=10)

        # Navigation Frame for Week Control
        exp_nav_frame = tk.Frame(expenses_history_frame, bg="white")
        exp_nav_frame.pack(pady=10)
        prev_week_btn = tk.Button(exp_nav_frame, text="<", font=("Helvetica", 14), command=self.previous_week)
        prev_week_btn.pack(side="left", padx=5)
        self.week_label = tk.Label(exp_nav_frame, text="", font=("Helvetica", 14), bg="white")
        self.week_label.pack(side="left", padx=5)
        next_week_btn = tk.Button(exp_nav_frame, text=">", font=("Helvetica", 14), command=self.next_week)
        next_week_btn.pack(side="left", padx=5)

        # Date Entry for Manual Week Selection
        tk.Label(expenses_history_frame, text="Enter Date (YYYY-MM-DD):", font=("Helvetica", 14), bg="white").pack(pady=(20,5))
        self.week_entry = tk.Entry(expenses_history_frame, font=("Helvetica", 14))
        self.week_entry.pack(pady=5)
        tk.Button(expenses_history_frame, text="Go", font=("Helvetica", 14), command=self.set_week_from_entry).pack(pady=5)

        # Table to Display Expenses History
        columns = ("Date", "Expense Type", "Amount")
        self.expenses_tree = ttk.Treeview(expenses_history_frame, columns=columns, show="headings")
        for col in columns:
            self.expenses_tree.heading(col, text=col)
        self.expenses_tree.pack(fill="both", expand=True, padx=10, pady=10)

        # Placeholder for No Records
        self.expenses_placeholder = tk.Label(expenses_history_frame, text="", font=("Helvetica", 12), bg="white")
        self.expenses_placeholder.pack(pady=20)

        # Update the Display
        self.update_expenses_history_display()

        # -------------------------------
        # Merchandise History Tab (Weekly)
        # -------------------------------
        merch_history_frame = tk.Frame(content_frame, bg="white")
        merch_history_frame.grid(row=0, column=0, sticky="nsew")
        tabs["Merchandise History"] = merch_history_frame

        tk.Label(merch_history_frame, text="Merchandise History", font=("Helvetica", 18), bg="white").pack(pady=10)

        # Navigation Frame for Week Control
        merch_nav_frame = tk.Frame(merch_history_frame, bg="white")
        merch_nav_frame.pack(pady=10)
        prev_merch_btn = tk.Button(merch_nav_frame, text="<", font=("Helvetica", 14), command=self.previous_merch_week)
        prev_merch_btn.pack(side="left", padx=5)
        self.merch_week_label = tk.Label(merch_nav_frame, text="", font=("Helvetica", 14), bg="white")
        self.merch_week_label.pack(side="left", padx=5)
        next_merch_btn = tk.Button(merch_nav_frame, text=">", font=("Helvetica", 14), command=self.next_merch_week)
        next_merch_btn.pack(side="left", padx=5)

        # Date Entry for Manual Week Selection
        tk.Label(merch_history_frame, text="Enter Date (YYYY-MM-DD):", font=("Helvetica", 14), bg="white").pack(pady=(20,5))
        self.merch_week_entry = tk.Entry(merch_history_frame, font=("Helvetica", 14))
        self.merch_week_entry.pack(pady=5)
        tk.Button(merch_history_frame, text="Go", font=("Helvetica", 14), command=self.set_merch_week_from_entry).pack(pady=5)

        # Table to Display Merchandise History
        columns = ("Date", "Merchandise Type", "Amount")
        self.merch_tree = ttk.Treeview(merch_history_frame, columns=columns, show="headings")
        for col in columns:
            self.merch_tree.heading(col, text=col)
        self.merch_tree.pack(fill="both", expand=True, padx=10, pady=10)

        # Placeholder for No Records
        self.merch_placeholder = tk.Label(merch_history_frame, text="", font=("Helvetica", 12), bg="white")
        self.merch_placeholder.pack(pady=20)

        # Update the Display
        self.update_merch_history_display()

        # -------------------------------
        # Gross Profit Tab (Weekly)
        # -------------------------------
        gross_profit_frame = tk.Frame(content_frame, bg="white")
        gross_profit_frame.grid(row=0, column=0, sticky="nsew")
        tabs["Gross Profit"] = gross_profit_frame

        tk.Label(gross_profit_frame, text="Gross Profit", font=("Helvetica", 18), bg="white").pack(pady=10)

        # Navigation Frame for Week Control
        profit_nav_frame = tk.Frame(gross_profit_frame, bg="white")
        profit_nav_frame.pack(pady=10)
        prev_profit_btn = tk.Button(profit_nav_frame, text="<", font=("Helvetica", 14), command=self.previous_profit_week)
        prev_profit_btn.pack(side="left", padx=5)
        self.profit_week_label = tk.Label(profit_nav_frame, text="", font=("Helvetica", 14), bg="white")
        self.profit_week_label.pack(side="left", padx=5)
        next_profit_btn = tk.Button(profit_nav_frame, text=">", font=("Helvetica", 14), command=self.next_profit_week)
        next_profit_btn.pack(side="left", padx=5)

        # Date Entry for Manual Week Selection
        tk.Label(gross_profit_frame, text="Enter Date (YYYY-MM-DD):", font=("Helvetica", 14), bg="white").pack(pady=(20,5))
        self.profit_week_entry = tk.Entry(gross_profit_frame, font=("Helvetica", 14))
        self.profit_week_entry.pack(pady=5)
        tk.Button(gross_profit_frame, text="Go", font=("Helvetica", 14), command=self.set_profit_week_from_entry).pack(pady=5)

        # Table to Display Gross Profit
        columns = ("Date", "Cash", "Credit", "Total")
        self.gross_profit_tree = ttk.Treeview(gross_profit_frame, columns=columns, show="headings")
        for col in columns:
            self.gross_profit_tree.heading(col, text=col)
        self.gross_profit_tree.pack(fill="both", expand=True, padx=10, pady=10)

        # Update the Display
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

        # Navigation Frame for Payroll Week Control
        payroll_nav_frame = tk.Frame(payroll_frame, bg="white")
        payroll_nav_frame.pack(pady=10)
        payroll_prev_btn = tk.Button(payroll_nav_frame, text="<", font=("Helvetica", 14), command=self.previous_payroll_week)
        payroll_prev_btn.pack(side="left", padx=5)
        self.payroll_date_label = tk.Label(payroll_nav_frame, text=self.current_payroll_sunday.strftime("%Y-%m-%d"), font=("Helvetica", 14), bg="white")
        self.payroll_date_label.pack(side="left", padx=5)
        payroll_next_btn = tk.Button(payroll_nav_frame, text=">", font=("Helvetica", 14), command=self.next_payroll_week)
        payroll_next_btn.pack(side="left", padx=5)

        # Date Entry for Manual Payroll Week Selection
        tk.Label(payroll_frame, text="Enter Date (YYYY-MM-DD):", font=("Helvetica", 14), bg="white").pack(pady=(20,5))
        self.payroll_date_entry = tk.Entry(payroll_frame, font=("Helvetica", 14))
        self.payroll_date_entry.pack(pady=5)
        tk.Button(payroll_frame, text="Go", font=("Helvetica", 14), command=self.set_payroll_date_from_entry).pack(pady=5)

        # Table to Display Payroll History
        columns = ("Date", "Pay")
        self.payroll_tree = ttk.Treeview(payroll_frame, columns=columns, show="headings")
        for col in columns:
            self.payroll_tree.heading(col, text=col)
        self.payroll_tree.pack(fill="both", expand=True, padx=10, pady=10)

        # Update the Display
        self.update_payroll_display()

        # -------------------------------
        # Function to Show Selected Tab
        # -------------------------------
        def show_tab(tab_name):
            tabs[tab_name].tkraise()

        # Add buttons for each tab in the left panel
        for title in tabs:
            btn = tk.Button(tab_frame, text=title, font=("Helvetica", 14), fg="black", bg="white",
                            relief="solid", bd=2, command=lambda t=title: show_tab(t), width=25, height=2)
            btn.pack(pady=5, padx=10, fill="x")

        # Show the default tab
        show_tab("Enter Invoice")

    # -------------------------------
    # Bottom Frame (Logout Button)
    # -------------------------------
    def create_bottom_frame(self):
        """Creates a bottom frame for the logout button."""
        bottom_frame = tk.Frame(self, bg="white", bd=1, relief="solid")
        bottom_frame.pack(side="bottom", fill="x", padx=10, pady=10)

        logout_button = tk.Button(bottom_frame, text="Logout", font=("Helvetica", 14), bg="red", fg="white",
                                  command=self.logout)
        logout_button.pack(side="left", padx=10, pady=5)

    # -------------------------------
    # Logout Method
    # -------------------------------
    def logout(self):
        """Handles logout and returns to the login page."""
        confirm = messagebox.askyesno("Logout", "Are you sure you want to logout?")
        if confirm:
            self.controller.show_frame("LoginPage")

    # -------------------------------
    # Employee History Methods
    # -------------------------------
    def update_history_display(self):
        """Updates the employee history table with data for the current date."""
        # Clear the table
        for row in self.history_tree.get_children():
            self.history_tree.delete(row)

        # Placeholder data (replace with actual data from your database)
        placeholder_data = [
            ("Alice", "09:00 AM", "05:00 PM", "8.0"),
            ("Bob", "10:00 AM", "06:00 PM", "8.0"),
            ("Charlie", "08:30 AM", "04:30 PM", "8.0"),
        ]

        if placeholder_data:
            # Insert data into the table
            for data in placeholder_data:
                self.history_tree.insert("", "end", values=data)
            self.history_placeholder.config(text="")
        else:
            # Show a message if no records are found
            self.history_placeholder.config(text=f"No clock-in records for {self.current_date.strftime('%Y-%m-%d')}.")

    def previous_day(self):
        """Navigates to the previous day."""
        self.current_date -= timedelta(days=1)
        self.date_label.config(text=self.current_date.strftime("%Y-%m-%d"))
        self.update_history_display()

    def next_day(self):
        """Navigates to the next day."""
        self.current_date += timedelta(days=1)
        self.date_label.config(text=self.current_date.strftime("%Y-%m-%d"))
        self.update_history_display()

    def set_date_from_entry(self):
        """Sets the date based on user input."""
        try:
            new_date = datetime.strptime(self.date_entry.get(), "%Y-%m-%d").date()
            self.current_date = new_date
            self.date_label.config(text=self.current_date.strftime("%Y-%m-%d"))
            self.update_history_display()
        except ValueError:
            messagebox.showerror("Invalid Date", "Please enter a valid date in YYYY-MM-DD format.")

    # -------------------------------
    # Expenses History Methods
    # -------------------------------
    def update_expenses_history_display(self):
        """Updates the expenses history table with data for the current week."""
        # Clear the table
        for row in self.expenses_tree.get_children():
            self.expenses_tree.delete(row)

        # Placeholder data (replace with actual data from your database)
        placeholder_data = [
            ("2023-10-02", "Supplies", "$100"),
            ("2023-10-03", "Utilities", "$200"),
            ("2023-10-04", "Maintenance", "$150"),
        ]

        if placeholder_data:
            # Insert data into the table
            for data in placeholder_data:
                self.expenses_tree.insert("", "end", values=data)
            self.expenses_placeholder.config(text="")
        else:
            # Show a message if no records are found
            week_end = self.current_week_start + timedelta(days=6)
            self.expenses_placeholder.config(
                text=f"No expenses recorded for the week of {self.current_week_start.strftime('%Y-%m-%d')} to {week_end.strftime('%Y-%m-%d')}.")

    def previous_week(self):
        """Navigates to the previous week."""
        self.current_week_start -= timedelta(weeks=1)
        self.update_expenses_history_display()

    def next_week(self):
        """Navigates to the next week."""
        self.current_week_start += timedelta(weeks=1)
        self.update_expenses_history_display()

    def set_week_from_entry(self):
        """Sets the week based on user input."""
        try:
            new_date = datetime.strptime(self.week_entry.get(), "%Y-%m-%d").date()
            self.current_week_start = new_date - timedelta(days=new_date.weekday())
            self.update_expenses_history_display()
        except ValueError:
            messagebox.showerror("Invalid Date", "Please enter a valid date in YYYY-MM-DD format.")

    # -------------------------------
    # Merchandise History Methods
    # -------------------------------
    def update_merch_history_display(self):
        """Updates the merchandise history table with data for the current week."""
        # Clear the table
        for row in self.merch_tree.get_children():
            self.merch_tree.delete(row)

        # Placeholder data (replace with actual data from your database)
        placeholder_data = [
            ("2023-10-02", "Electronics", "$500"),
            ("2023-10-03", "Clothing", "$300"),
            ("2023-10-04", "Furniture", "$700"),
        ]

        if placeholder_data:
            # Insert data into the table
            for data in placeholder_data:
                self.merch_tree.insert("", "end", values=data)
            self.merch_placeholder.config(text="")
        else:
            # Show a message if no records are found
            merch_week_end = self.current_merch_week_start + timedelta(days=6)
            self.merch_placeholder.config(
                text=f"No merchandise recorded for the week of {self.current_merch_week_start.strftime('%Y-%m-%d')} to {merch_week_end.strftime('%Y-%m-%d')}.")

    def previous_merch_week(self):
        """Navigates to the previous merchandise week."""
        self.current_merch_week_start -= timedelta(weeks=1)
        self.update_merch_history_display()

    def next_merch_week(self):
        """Navigates to the next merchandise week."""
        self.current_merch_week_start += timedelta(weeks=1)
        self.update_merch_history_display()

    def set_merch_week_from_entry(self):
        """Sets the merchandise week based on user input."""
        try:
            new_date = datetime.strptime(self.merch_week_entry.get(), "%Y-%m-%d").date()
            self.current_merch_week_start = new_date - timedelta(days=new_date.weekday())
            self.update_merch_history_display()
        except ValueError:
            messagebox.showerror("Invalid Date", "Please enter a valid date in YYYY-MM-DD format.")

    # -------------------------------
    # Gross Profit Methods
    # -------------------------------
    def update_gross_profit_display(self):
        """Updates the gross profit table with data for the current week."""
        # Clear the table
        for row in self.gross_profit_tree.get_children():
            self.gross_profit_tree.delete(row)

        # Placeholder data (replace with actual data from your database)
        placeholder_data = [
            ("2023-10-02", "$1000", "$500", "$1500"),
            ("2023-10-03", "$1200", "$600", "$1800"),
            ("2023-10-04", "$900", "$400", "$1300"),
        ]

        if placeholder_data:
            # Insert data into the table
            for data in placeholder_data:
                self.gross_profit_tree.insert("", "end", values=data)
        else:
            # Show a message if no records are found
            profit_week_end = self.current_profit_week_start + timedelta(days=6)
            self.profit_week_label.config(text=f"{self.current_profit_week_start.strftime('%Y-%m-%d')} to {profit_week_end.strftime('%Y-%m-%d')}")

    def previous_profit_week(self):
        """Navigates to the previous profit week."""
        self.current_profit_week_start -= timedelta(weeks=1)
        self.update_gross_profit_display()

    def next_profit_week(self):
        """Navigates to the next profit week."""
        self.current_profit_week_start += timedelta(weeks=1)
        self.update_gross_profit_display()

    def set_profit_week_from_entry(self):
        """Sets the profit week based on user input."""
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
        """Returns the most recent Sunday for a given date."""
        days_since_sunday = (d.weekday() + 1) % 7
        return d - timedelta(days=days_since_sunday)

    def update_payroll_display(self):
        """Updates the payroll table with data for the current payroll week."""
        # Clear the table
        for row in self.payroll_tree.get_children():
            self.payroll_tree.delete(row)

        # Placeholder data (replace with actual data from your database)
        placeholder_data = [
            ("2023-10-01", "$1200"),
            ("2023-09-24", "$1100"),
            ("2023-09-17", "$1000"),
            ("2023-09-10", "$950"),
        ]

        if placeholder_data:
            # Insert data into the table
            for data in placeholder_data:
                self.payroll_tree.insert("", "end", values=data)
        else:
            # Show a message if no records are found
            self.payroll_date_label.config(text=self.current_payroll_sunday.strftime("%Y-%m-%d"))

    def previous_payroll_week(self):
        """Navigates to the previous payroll week."""
        self.current_payroll_sunday -= timedelta(weeks=1)
        self.payroll_date_label.config(text=self.current_payroll_sunday.strftime("%Y-%m-%d"))
        self.update_payroll_display()

    def next_payroll_week(self):
        """Navigates to the next payroll week."""
        self.current_payroll_sunday += timedelta(weeks=1)
        self.payroll_date_label.config(text=self.current_payroll_sunday.strftime("%Y-%m-%d"))
        self.update_payroll_display()

    def set_payroll_date_from_entry(self):
        """Sets the payroll date based on user input."""
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