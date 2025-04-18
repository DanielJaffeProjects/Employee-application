import tkinter as tk
from tkinter import ttk, messagebox
import re

import sqlConnector

def create_withdraw_tab(content_frame, tabs):
    """Creates the Withdraw tab and adds it to the tabs dictionary."""
    withdraw_frame = tk.Frame(content_frame, bg="white")
    withdraw_frame.grid(row=0, column=0, sticky="nsew")
    tabs["Withdraw"] = withdraw_frame

    # Title
    tk.Label(withdraw_frame, text="Manage Withdrawals", font=("Helvetica", 18), bg="white").pack(pady=10)


    # Form Fields
    tk.Label(withdraw_frame, text="Withdraw ID:", font=("Helvetica", 14), bg="white").pack()
    withdraw_id_entry = tk.Entry(withdraw_frame, font=("Helvetica", 14))
    withdraw_id_entry.pack()

    tk.Label(withdraw_frame, text="Employee ID:", font=("Helvetica", 14), bg="white").pack()
    employee_id_entry = tk.Entry(withdraw_frame, font=("Helvetica", 14))
    employee_id_entry.pack()

    tk.Label(withdraw_frame, text="Store ID:", font=("Helvetica", 14), bg="white").pack()
    store_id_entry = tk.Entry(withdraw_frame, font=("Helvetica", 14))
    store_id_entry.pack()

    tk.Label(withdraw_frame, text="Withdraw Date (YYYY-MM-DD):", font=("Helvetica", 14), bg="white").pack()
    withdraw_date_entry = tk.Entry(withdraw_frame, font=("Helvetica", 14))
    withdraw_date_entry.pack()

    tk.Label(withdraw_frame, text="Amount:", font=("Helvetica", 14), bg="white").pack()
    amount_entry = tk.Entry(withdraw_frame, font=("Helvetica", 14))
    amount_entry.pack()

    # Submit Button
    tk.Button(withdraw_frame, text="Add Withdrawal", font=("Helvetica", 14),
              command=lambda: add_withdrawal(withdraw_id_entry.get(),employee_id_entry.get(), store_id_entry.get(),
                                            withdraw_date_entry.get(), amount_entry.get())).pack(pady=10)

    # another secret Easter egg from the great Jaffe
    # Treeview for Displaying Withdrawals
    withdraw_tree = ttk.Treeview(withdraw_frame, columns=("WithdrawID", "EmployeeID", "StoreID", "WithdrawDate", "Amount"),
                                  show="headings")
    withdraw_tree.heading("WithdrawID", text="Withdraw ID")
    withdraw_tree.heading("EmployeeID", text="Employee ID")
    withdraw_tree.heading("StoreID", text="Store ID")
    withdraw_tree.heading("WithdrawDate", text="Withdraw Date")
    withdraw_tree.heading("Amount", text="Amount")
    withdraw_tree.pack(fill="both", expand=True, padx=10, pady=10)

    # Load Withdrawals Button
    tk.Button(withdraw_frame, text="Load Withdrawals", font=("Helvetica", 14),
              command=lambda: load_withdrawals(withdraw_tree)).pack(pady=10)

def add_withdrawal(withdraw_id, employee_id, store_id, withdraw_date, amount):
    """Adds a new withdrawal record to the database."""
    if  not withdraw_id or not employee_id or not store_id or not withdraw_date or not amount:
        messagebox.showerror("Error", "All fields are required.")
        return

    # Validate withdraw_id
    if not withdraw_id.isdigit():
        messagebox.showerror("Error", "Withdraw ID must be a numeric value.")
        return

    # Check if withdraw_id already exists
    try:
        query = "SELECT COUNT(*) FROM withdraw WHERE withdraw_id = %s"
        result = sqlConnector.connect(query, (withdraw_id,))
        if result[0][0] > 0:
            messagebox.showerror("Error", "Withdraw ID already exists in the database.")
            return
    except Exception as e:
        messagebox.showerror("Error", f"Failed to validate Withdraw ID: {e}")
        return


    # Validate employee_id and store_id
    try:
        employee_id = int(employee_id)
        store_id = int(store_id)
    except ValueError:
        messagebox.showerror("Error", "Employee ID and Store ID must be integers.")
        return

    # Validate employee_id exists
    try:
        employee_id = int(employee_id)
        query = "SELECT COUNT(*) FROM employee WHERE employee_id = %s"
        result = sqlConnector.connect(query, (employee_id,))
        if result[0][0] == 0:
            messagebox.showerror("Error", "Invalid Employee ID.")
            return
    except ValueError:
        messagebox.showerror("Error", "Employee ID must be an integer.")
        return

    # Validate store_id exists
    try:
        store_id = int(store_id)
        query = "SELECT COUNT(*) FROM store WHERE store_id = %s"
        result = sqlConnector.connect(query, (store_id,))
        if result[0][0] == 0:
            messagebox.showerror("Error", "Invalid Store ID.")
            return
    except ValueError:
        messagebox.showerror("Error", "Store ID must be an integer.")
        return

        # Validate withdraw_date format
    if not re.match(r"^\d{4}-\d{2}-\d{2}$", withdraw_date):
        messagebox.showerror("Error", "Withdraw Date must be in YYYY-MM-DD format.")
        return

        # Validate amount
    try:
        amount = float(amount)
        if amount <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Error", "Amount must be a positive number.")
        return

    try:
        query = """INSERT INTO withdraw (withdraw_id,employee_id, store_id, withdraw_date, amount)
                   VALUES (%s,%s, %s, %s, %s)"""
        data = (withdraw_id,int(employee_id), int(store_id), withdraw_date, float(amount))
        sqlConnector.connect(query, data)
        messagebox.showinfo("Success", "Withdrawal added successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to add withdrawal: {e}")

def load_withdrawals(tree):

    """Loads all withdrawal records into the Treeview."""
    try:
        query = "SELECT * FROM withdraw"
        results = sqlConnector.connect(query, ())
        # Clear existing rows
        for row in tree.get_children():
            tree.delete(row)
        # Insert new rows
        for result in results:
            tree.insert("", "end", values=result)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load withdrawals: {e}")