import tkinter as tk
from datetime import datetime
from tkinter import messagebox, ttk
import sqlConnector
import re

def create_merchandise_tab(content_frame, tabs):
    # Create Merchandise Tab
    enter_merch_frame = tk.Frame(content_frame, bg="white")
    enter_merch_frame.grid(row=0, column=0, sticky="nsew")
    tk.Label(enter_merch_frame, text="Enter Merchandise", font=("Helvetica", 18), bg="white").pack(pady=10)

    # Merchandise Type
    tk.Label(enter_merch_frame, text="Merchandise Type:", font=("Helvetica", 14), bg="white").pack()
    merch_type = tk.Entry(enter_merch_frame, font=("Helvetica", 14))
    merch_type.pack()

    # Merchandise Value
    tk.Label(enter_merch_frame, text="Merchandise Value:", font=("Helvetica", 14), bg="white").pack()
    merch_value = tk.Entry(enter_merch_frame, font=("Helvetica", 14))
    merch_value.pack()

    # Purchase Date
    tk.Label(enter_merch_frame, text="Purchase Date (YYYY-MM-DD):", font=("Helvetica", 14), bg="white").pack()
    purchase_date = tk.Entry(enter_merch_frame, font=("Helvetica", 14))
    purchase_date.pack()

    # Store ID
    tk.Label(enter_merch_frame, text="Store ID:", font=("Helvetica", 14), bg="white").pack()
    store_id = tk.Entry(enter_merch_frame, font=("Helvetica", 14))
    store_id.pack()

    # Submit Button
    tk.Button(enter_merch_frame, text="Submit Merchandise", font=("Helvetica", 14),
              command=lambda: submit_merchandise(merch_type.get(), merch_value.get(), purchase_date.get(),
                                                 store_id.get())).pack(pady=10)
    # Merchandise Records Treeview
    tk.Label(enter_merch_frame, text="Merchandise Records", font=("Helvetica", 14), bg="white").pack(pady=10)
    merch_tree = ttk.Treeview(enter_merch_frame, columns=("Type", "Value", "Date", "Store ID"), show="headings")
    merch_tree.pack(fill="both", expand=True, padx=10, pady=5)

    # Define columns
    merch_tree.heading("Type", text="Merchandise Type")
    merch_tree.heading("Value", text="Value")
    merch_tree.heading("Date", text="Purchase Date")
    merch_tree.heading("Store ID", text="Store ID")

    merch_tree.column("Type", width=150, anchor="center")
    merch_tree.column("Value", width=100, anchor="center")
    merch_tree.column("Date", width=120, anchor="center")
    merch_tree.column("Store ID", width=100, anchor="center")

    # Load Merchandise Records Button
    tk.Button(enter_merch_frame, text="Load Merchandise Records", font=("Helvetica", 14),
              command=lambda: load_merchandise_records(merch_tree)).pack(pady=10)
    tabs["Enter Merchandise"] = enter_merch_frame

def submit_merchandise(merch_type, merch_value, purchase_date, store_id):
    if not merch_type or not merch_value or not purchase_date:
        messagebox.showerror("Error", "All fields except Store ID must be filled out.")
        return

    # Validate Merchandise Type
    if not merch_type or not re.match(r"^[a-zA-Z0-9\s]+$", merch_type):
        messagebox.showerror("Error", "Merchandise Type must be alphanumeric and not empty.")
        return

    # Validate Merchandise Value
    try:
        merch_value = float(merch_value)
        if merch_value <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Error", "Merchandise Value must be a positive number.")
        return

    # Validate Purchase Date
    try:
        datetime.strptime(purchase_date, "%Y-%m-%d")
    except ValueError:
        messagebox.showerror("Error", "Purchase Date must be in the format YYYY-MM-DD and valid.")
        return

    # Validate Store ID
    if store_id:
        try:
            query = "SELECT COUNT(*) FROM Store WHERE store_id = %s"
            data = (store_id,)
            result = sqlConnector.connect(query, data)
            if not result or result[0][0] == 0:
                messagebox.showerror("Error", "Store ID does not exist in the database.")
                return
        except Exception as e:
            messagebox.showerror("Error", f"Failed to validate Store ID: {e}")
            return

    try:
        # SQL query to insert merchandise data
        query = """
        INSERT INTO Merchandise (Merch_Type, Merch_Value, Purchase_Date, StoreID)
        VALUES (%s, %s, %s, %s)
        """
        data = (merch_type, float(merch_value), purchase_date, store_id)

        # Execute the query
        sqlConnector.connect(query, data)

        messagebox.showinfo("Success", "Merchandise added successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to add merchandise: {e}")


def load_merchandise_records(merch_tree):
    """Loads merchandise records into the Treeview."""
    try:
        query = "SELECT Merch_Type, Merch_Value, Purchase_Date, StoreID FROM Merchandise"
        data = ()
        records = sqlConnector.connect(query,data)
        merch_tree.delete(*merch_tree.get_children())  # Clear existing records
        for record in records:
            merch_tree.insert("", "end", values=record)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load merchandise records: {e}")