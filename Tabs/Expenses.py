import tkinter as tk
from datetime import datetime
from tkinter import ttk
from Main import sqlConnector
from Main.Notification import show_notification


def create_expenses_tab(content_frame, tabs):
    """Creates the Expenses tab and adds it to the tabs dictionary."""
    expenses_frame = tk.Frame(content_frame, bg="white")
    expenses_frame.grid(row=0, column=0, sticky="nsew")
    tabs["Expenses"] = expenses_frame

    # Title
    tk.Label(expenses_frame, text="Manage Expenses", font=("Helvetica", 18), bg="white").pack(pady=10)

    # Form Fields
    tk.Label(expenses_frame, text="Expense Type:", font=("Helvetica", 14), bg="white").pack()
    expense_type_entry = tk.Entry(expenses_frame, font=("Helvetica", 14))
    expense_type_entry.pack()

    tk.Label(expenses_frame, text="Expense Value:", font=("Helvetica", 14), bg="white").pack()
    expense_value_entry = tk.Entry(expenses_frame, font=("Helvetica", 14))
    expense_value_entry.pack()

    tk.Label(expenses_frame, text="Expense Date (YYYY-MM-DD):", font=("Helvetica", 14), bg="white").pack()
    expense_date_entry = tk.Entry(expenses_frame, font=("Helvetica", 14))
    expense_date_entry.pack()

    # Employee Name Dropdown
    tk.Label(expenses_frame, text="Employee Name:", font=("Helvetica", 14), bg="white").pack()
    employee_name_var = tk.StringVar(expenses_frame)
    employee_name_dropdown = ttk.Combobox(expenses_frame, textvariable=employee_name_var, font=("Helvetica", 14), state="readonly")
    employee_name_dropdown.pack()

    # Store Name Dropdown
    tk.Label(expenses_frame, text="Store Name:", font=("Helvetica", 14), bg="white").pack()
    store_name_var = tk.StringVar(expenses_frame)
    store_name_dropdown = ttk.Combobox(expenses_frame, textvariable=store_name_var, font=("Helvetica", 14), state="readonly")
    store_name_dropdown.pack()

    # Populate dropdowns
    employee_mapping = load_employee_names()
    employee_name_dropdown['values'] = list(employee_mapping.keys())

    store_mapping = load_store_names()
    store_name_dropdown['values'] = list(store_mapping.keys())

    # Submit Button
    tk.Button(expenses_frame, text="Add Expense", font=("Helvetica", 14),
              command=lambda: add_expense(expense_type_entry.get(), expense_value_entry.get(),
                                          expense_date_entry.get(), employee_mapping.get(employee_name_var.get()),
                                          store_mapping.get(store_name_var.get()))).pack(pady=10)

    # Treeview for Displaying Expenses
    columns = ("ExpenseID", "EmployeeName", "StoreName", "ExpenseDate", "ExpenseType", "Amount")
    expenses_tree = ttk.Treeview(expenses_frame, columns=columns, show="headings")
    for col in columns:
        expenses_tree.heading(col, text=col)
    expenses_tree.column(col, width=120, anchor="center")
    expenses_tree.pack(fill="both", expand=True, padx=10, pady=10)

    # Load Expenses Button
    tk.Button(expenses_frame, text="Load Expenses", font=("Helvetica", 14),
              command=lambda: load_expenses(expenses_tree)).pack(pady=10)


def add_expense(expense_type, expense_value, expense_date, employee_id, store_id):
    """Adds a new expense record to the database."""
    if not expense_type or not expense_value or not expense_date or not employee_id or not store_id:
        show_notification("All fields are required.")
        return


    # Validate inputs
    try:
        expense_value = float(expense_value)
        employee_id = int(employee_id)
        store_id = int(store_id)
    except ValueError:
        show_notification("Please enter valid numeric values for Expense Value, Employee ID, and Store ID.")
        return

    # Validate date format
    try:
        datetime.strptime(expense_date, "%Y-%m-%d")
    except ValueError:
        show_notification("Please enter a valid date in the format YYYY-MM-DD.")
        return
    # Validate Employee ID
    try:
        emp_check_query = "SELECT COUNT(*) FROM Employee WHERE employee_id = %s"
        emp_exists = sqlConnector.connect(emp_check_query, (employee_id,))
        if emp_exists[0][0] == 0:
            show_notification( "Employee ID not found.")
            return
    except Exception as e:
        show_notification("Failed to validate Employee ID: {e}")
        return

    # Validate Store ID
    try:
        store_check_query = "SELECT COUNT(*) FROM Store WHERE store_id = %s"
        store_exists = sqlConnector.connect(store_check_query, (store_id,))
        if store_exists[0][0] == 0:
            show_notification("Store ID not found.")
            return
    except Exception as e:
        show_notification("Failed to validate Store ID: {e}")
        return

    try:
        query = """INSERT INTO Expense (expense_type, amount, expense_date, employee_id, store_id)
                   VALUES (%s, %s, %s, %s, %s)"""
        data = (expense_type, float(expense_value), expense_date, int(employee_id), int(store_id))
        sqlConnector.connect(query, data)
        show_notification( "Expense added successfully!")
    except Exception as e:
        show_notification("Failed to add expense: {e}")

def load_employee_names():
    """Loads employee names (concatenated first and last names) and their IDs from the database."""
    try:
        query = "SELECT employee_id, CONCAT(firstName, ' ', lastName) AS employee_name FROM Employee"
        results = sqlConnector.connect(query, ())
        return {employee_name: employee_id for employee_id, employee_name in results}
    except Exception as e:
        show_notification(f"Failed to load employee names: {e}")
        return {}


def load_expenses(tree):
    """Loads all expense records into the Treeview with employee and store names."""
    try:
        query = """SELECT e.expense_id, 
                          CONCAT(emp.firstName, ' ', emp.lastName) AS employee_name, 
                          s.store_name, 
                          e.expense_date, 
                          e.expense_type, 
                          e.amount
                   FROM Expense e
                   JOIN Employee emp ON e.employee_id = emp.employee_id
                   JOIN Store s ON e.store_id = s.store_id"""
        results = sqlConnector.connect(query, ())
        # Clear existing rows
        for row in tree.get_children():
            tree.delete(row)
        # Insert new rows
        for result in results:
            tree.insert("", "end", values=result)
    except Exception as e:
        show_notification(f"Failed to load expenses: {e}")

def load_store_names():
    """Loads store names and their IDs from the database."""
    try:
        query = "SELECT store_id, store_name FROM Store"  # Ensure table name matches the schema
        results = sqlConnector.connect(query, ())
        return {store_name: store_id for store_id, store_name in results}
    except Exception as e:
        show_notification(f"Failed to load store names: {e}")
        return {}