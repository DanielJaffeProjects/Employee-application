import tkinter as tk
from datetime import datetime
from tkinter import messagebox, ttk
from Main import sqlConnector
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

    # Store Dropdown
    tk.Label(enter_merch_frame, text="Store:", font=("Helvetica", 14), bg="white").pack()
    store_var = tk.StringVar()
    store_dropdown = ttk.Combobox(enter_merch_frame, textvariable=store_var, font=("Helvetica", 14))
    store_dropdown.pack()

    # Populate the dropdown with store names and IDs
    store_map = {}
    try:
        query = "SELECT store_id, store_name FROM Store"
        result = sqlConnector.connect(query,())
        store_map = {f"{row[1]} (ID: {row[0]})": row[0] for row in result}
        store_dropdown['values'] = list(store_map.keys())
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load stores: {e}")

    # Submit Button
    tk.Button(enter_merch_frame, text="Submit Merchandise", font=("Helvetica", 14),
              command=lambda: submit_merchandise(merch_type.get(), merch_value.get(), purchase_date.get(),
                                                 store_map.get(store_var.get()))).pack(pady=10)

    # Merchandise Records Treeview
    tk.Label(enter_merch_frame, text="Merchandise Records", font=("Helvetica", 14), bg="white").pack(pady=10)
    merch_tree = ttk.Treeview(
        enter_merch_frame,
        columns=("Type", "Value", "Date", "Store ID", "Store Name"),  # Include "Store Name" here
        show="headings"
    )
    merch_tree.pack(fill="both", expand=True, padx=10, pady=5)

    # Define columns
    merch_tree.heading("Type", text="Merchandise Type")
    merch_tree.heading("Value", text="Value")
    merch_tree.heading("Date", text="Purchase Date")
    merch_tree.heading("Store ID", text="Store ID")
    merch_tree.heading("Store Name", text="Store Name")  # This will now work correctly

    merch_tree.column("Type", width=150, anchor="center")
    merch_tree.column("Value", width=100, anchor="center")
    merch_tree.column("Date", width=120, anchor="center")
    merch_tree.column("Store ID", width=150, anchor="center")
    merch_tree.column("Store Name", width=150, anchor="center")

    # Load Merchandise Records Button
    tk.Button(enter_merch_frame, text="Load Merchandise Records", font=("Helvetica", 14),
              command=lambda: load_merchandise_records(merch_tree)).pack(pady=10)
    tabs["Enter Merchandise"] = enter_merch_frame

def submit_merchandise(merch_type, merch_value, purchase_date, store_id):
    if not merch_type or not merch_value or not purchase_date or not store_id:
        messagebox.showerror("Error", "All fields must be filled out.")
        return

    # Validate Merchandise Type
    if not re.match(r"^[a-zA-Z0-9\s]+$", merch_type):
        messagebox.showerror("Error", "Merchandise Type must be alphanumeric.")
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
        messagebox.showerror("Error", "Purchase Date must be in the format YYYY-MM-DD.")
        return

    try:
        # SQL query to insert merchandise data
        query = """
        INSERT INTO Merchandise (Merch_Type, Merch_Value, Purchase_Date, StoreID)
        VALUES (%s, %s, %s, %s)
        """
        data = (merch_type, merch_value, purchase_date, store_id)

        # Execute the query
        sqlConnector.connect(query, data)

        messagebox.showinfo("Success", "Merchandise added successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to add merchandise: {e}")

def load_merchandise_records(merch_tree):
    """Loads merchandise records into the Treeview."""
    print("Loading merchandise records...")  # Debugging line
    try:
        # Query to fetch merchandise records
        merch_query = """SELECT Merch_Type, Merch_Value, Purchase_Date, StoreID
        FROM merchandise
        """
        merchandise_records = sqlConnector.connect(merch_query, ())
        print("Merchandise records fetched:", merchandise_records)  # Debugging line
        # Ensure merchandise_records is a list
        if not isinstance(merchandise_records, list):
            raise ValueError("Unexpected data type returned from merchandise query.")

        # Query to fetch store records
        store_query = """SELECT store_id, store_name
        FROM store
        """
        store_records = sqlConnector.connect(store_query, ())
        print("Store records fetched:", store_records)
        # Ensure store_records is a list
        if not isinstance(store_records, list):
            raise ValueError("Unexpected data type returned from store query.")

        # Create a mapping of StoreID to store_name
        store_map = {store[0]: store[1] for store in store_records}

        # Clear existing records in the Treeview
        merch_tree.delete(*merch_tree.get_children())

        # Combine merchandise records with store names
        for record in merchandise_records:
            store_name = store_map.get(record[3], "Unknown")  # Get store_name or "Unknown" if not found
            merch_tree.insert("", "end", values=(*record, store_name))

    except Exception as e:
        messagebox.showerror("Error", f"Failed to load merchandise records: {e}")