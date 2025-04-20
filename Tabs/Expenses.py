import tkinter as tk
from datetime import datetime
from tkinter import ttk, messagebox
from Main import sqlConnector


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

    tk.Label(expenses_frame, text="Employee ID:", font=("Helvetica", 14), bg="white").pack()
    employee_id_entry = tk.Entry(expenses_frame, font=("Helvetica", 14))
    employee_id_entry.pack()

    tk.Label(expenses_frame, text="Store ID:", font=("Helvetica", 14), bg="white").pack()
    store_id_entry = tk.Entry(expenses_frame, font=("Helvetica", 14))
    store_id_entry.pack()

    # Submit Button
    tk.Button(expenses_frame, text="Add Expense", font=("Helvetica", 14),
              command=lambda: add_expense(expense_type_entry.get(), expense_value_entry.get(),
                                          expense_date_entry.get(), employee_id_entry.get(),
                                          store_id_entry.get())).pack(pady=10)

    # Treeview for Displaying Expenses
    columns = ("ExpenseID", "EmployeeID", "StoreID", "ExpenseDate", "ExpenseType", "Amount")
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
        messagebox.showerror("Error", "All fields are required.")
        return


    # Validate inputs
    try:
        expense_value = float(expense_value)
        employee_id = int(employee_id)
        store_id = int(store_id)
    except ValueError:
        messagebox.showerror("Error", "Please enter valid numeric values for Expense Value, Employee ID, and Store ID.")
        return

    # Validate date format
    try:
        datetime.strptime(expense_date, "%Y-%m-%d")
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid date in the format YYYY-MM-DD.")
        return
    # Validate Employee ID
    try:
        emp_check_query = "SELECT COUNT(*) FROM Employee WHERE employee_id = %s"
        emp_exists = sqlConnector.connect(emp_check_query, (employee_id,))
        if emp_exists[0][0] == 0:
            messagebox.showerror("Error", "Employee ID not found.")
            return
    except Exception as e:
        messagebox.showerror("Error", f"Failed to validate Employee ID: {e}")
        return

    # Validate Store ID
    try:
        store_check_query = "SELECT COUNT(*) FROM Store WHERE store_id = %s"
        store_exists = sqlConnector.connect(store_check_query, (store_id,))
        if store_exists[0][0] == 0:
            messagebox.showerror("Error", "Store ID not found.")
            return
    except Exception as e:
        messagebox.showerror("Error", f"Failed to validate Store ID: {e}")
        return

    try:
        query = """INSERT INTO Expense (expense_type, amount, expense_date, employee_id, store_id)
                   VALUES (%s, %s, %s, %s, %s)"""
        data = (expense_type, float(expense_value), expense_date, int(employee_id), int(store_id))
        sqlConnector.connect(query, data)
        messagebox.showinfo("Success", "Expense added successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to add expense: {e}")

def load_expenses(tree):
    """Loads all expense records into the Treeview."""
    try:
        query = "SELECT * FROM Expense"
        results = sqlConnector.connect(query, ())
        # Clear existing rows
        for row in tree.get_children():
            tree.delete(row)
        # Insert new rows
        for result in results:
            tree.insert("", "end", values=result)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load expenses: {e}")