import tkinter as tk
from tkinter import ttk
import re
from Main import sqlConnector
from Main.Notification import show_notification


def create_withdraw_tab(content_frame, tabs):
    """Creates the Withdraw tab and adds it to the tabs dictionary."""
    withdraw_frame = tk.Frame(content_frame, bg="white")
    withdraw_frame.grid(row=0, column=0, sticky="nsew")
    tabs["Withdraw"] = withdraw_frame

    # Title
    tk.Label(withdraw_frame, text="Manage Withdrawals", font=("Helvetica", 18), bg="white").pack(pady=10)

    # Store Name Dropdown
    tk.Label(withdraw_frame, text="Store Name:", font=("Helvetica", 14), bg="white").pack()
    store_name_var = tk.StringVar(withdraw_frame)
    store_name_dropdown = ttk.Combobox(withdraw_frame, textvariable=store_name_var, font=("Helvetica", 14), state="readonly")
    store_name_dropdown.pack()

    # Populate the dropdown with store names
    store_mapping = load_store_names()
    store_name_dropdown['values'] = list(store_mapping.keys())

    # Withdraw Date Entry
    tk.Label(withdraw_frame, text="Withdraw Date (YYYY-MM-DD):", font=("Helvetica", 14), bg="white").pack()
    withdraw_date_entry = tk.Entry(withdraw_frame, font=("Helvetica", 14))
    withdraw_date_entry.pack()

    # Amount Entry
    tk.Label(withdraw_frame, text="Amount:", font=("Helvetica", 14), bg="white").pack()
    amount_entry = tk.Entry(withdraw_frame, font=("Helvetica", 14))
    amount_entry.pack()

    # Submit Button
    tk.Button(withdraw_frame, text="Add Withdrawal", font=("Helvetica", 14),
              command=lambda: add_withdrawal(store_mapping.get(store_name_var.get()),
                                             withdraw_date_entry.get(), amount_entry.get())).pack(pady=10)

    # Treeview for Displaying Withdrawals
    withdraw_tree = ttk.Treeview(withdraw_frame, columns=("StoreName", "WithdrawDate", "Amount"), show="headings")
    withdraw_tree.heading("StoreName", text="Store Name")
    withdraw_tree.heading("WithdrawDate", text="Withdraw Date")
    withdraw_tree.heading("Amount", text="Amount")
    withdraw_tree.pack(fill="both", expand=True, padx=10, pady=10)

    # Load Withdrawals Button
    tk.Button(withdraw_frame, text="Load Withdrawals", font=("Helvetica", 14),
              command=lambda: load_withdrawals(withdraw_tree)).pack(pady=10)


def add_withdrawal(store_id, withdraw_date, amount):
    """Adds a new withdrawal record to the database."""
    if not store_id or not withdraw_date or not amount:
        show_notification("All fields are required.")
        return

    # Validate store_id exists
    try:
        store_id = int(store_id)
        query = "SELECT COUNT(*) FROM store WHERE store_id = %s"
        result = sqlConnector.connect(query, (store_id,))
        if result[0][0] == 0:
            show_notification("Invalid Store ID.")
            return
    except ValueError:
        show_notification("Store ID must be an integer.")
        return

    # Validate withdraw_date format
    if not re.match(r"^\d{4}-\d{2}-\d{2}$", withdraw_date):
        show_notification("Withdraw Date must be in YYYY-MM-DD format.")
        return

    # Validate amount
    try:
        amount = float(amount)
        if amount <= 0:
            raise ValueError
    except ValueError:
        show_notification("Amount must be a positive number.")
        return

    # Insert withdrawal into the database
    try:
        query = """INSERT INTO withdraw (store_id, withdraw_date, amount)
                   VALUES (%s, %s, %s)"""
        data = (store_id, withdraw_date, amount)
        sqlConnector.connect(query, data)
        show_notification("Withdrawal added successfully!")
    except Exception as e:
        show_notification(f"Failed to add withdrawal: {e}")


def load_withdrawals(tree):
    """Loads withdrawal records with Store Name, Withdraw Date, and Amount into the Treeview."""
    try:
        # Query to join store and withdraw tables to get store_name
        query = """SELECT s.store_name, w.withdraw_date, w.amount
            FROM withdraw w
            JOIN store s ON w.store_id = s.store_id
        """
        results = sqlConnector.connect(query, ())

        # Clear existing rows in the Treeview
        for row in tree.get_children():
            tree.delete(row)

        # Insert new rows with store_name, withdraw_date, and amount
        for result in results:
            tree.insert("", "end", values=result)
    except Exception as e:
        show_notification(f"Failed to load withdrawals: {e}")


def load_store_names():
    """Loads store names and their IDs from the database."""
    try:
        query = "SELECT store_id, store_name FROM store"
        results = sqlConnector.connect(query, ())
        return {store_name: store_id for store_id, store_name in results}
    except Exception as e:
        show_notification(f"Failed to load store names: {e}")
        return {}