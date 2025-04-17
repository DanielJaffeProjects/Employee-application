import tkinter as tk
from tkinter import ttk, messagebox
import sqlConnector

def create_gross_profit_tab(content_frame, tabs):
    """Creates the Gross Profit tab and adds it to the tabs dictionary."""
    gross_profit_frame = tk.Frame(content_frame, bg="white")
    gross_profit_frame.grid(row=0, column=0, sticky="nsew")
    tabs["Gross Profit"] = gross_profit_frame

    # Title
    tk.Label(gross_profit_frame, text="Manage Gross Profit", font=("Helvetica", 18), bg="white").pack(pady=10)

    # Form Fields
    tk.Label(gross_profit_frame, text="Employee ID:", font=("Helvetica", 14), bg="white").pack()
    employee_id_entry = tk.Entry(gross_profit_frame, font=("Helvetica", 14))
    employee_id_entry.pack()

    tk.Label(gross_profit_frame, text="Store ID:", font=("Helvetica", 14), bg="white").pack()
    store_id_entry = tk.Entry(gross_profit_frame, font=("Helvetica", 14))
    store_id_entry.pack()

    tk.Label(gross_profit_frame, text="Date (YYYY-MM-DD):", font=("Helvetica", 14), bg="white").pack()
    date_entry = tk.Entry(gross_profit_frame, font=("Helvetica", 14))
    date_entry.pack()

    tk.Label(gross_profit_frame, text="Cash:", font=("Helvetica", 14), bg="white").pack()
    cash_entry = tk.Entry(gross_profit_frame, font=("Helvetica", 14))
    cash_entry.pack()

    tk.Label(gross_profit_frame, text="Credit:", font=("Helvetica", 14), bg="white").pack()
    credit_entry = tk.Entry(gross_profit_frame, font=("Helvetica", 14))
    credit_entry.pack()


    # Submit Button
    tk.Button(gross_profit_frame, text="Add Gross Profit", font=("Helvetica", 14),
              command=lambda: add_gross_profit(employee_id_entry.get(), store_id_entry.get(),
                                              date_entry.get(), cash_entry.get(),
                                              credit_entry.get())).pack(pady=10)

    # Treeview for Displaying Gross Profit Records
    gross_profit_tree = ttk.Treeview(
        gross_profit_frame,
        columns=("ProfitID", "EmployeeID", "StoreID", "Date", "Cash", "Credit", "Total"),
        show="headings"
    )

    # Set headings and column widths
    column_settings = {
        "ProfitID": 70,
        "EmployeeID": 90,
        "StoreID": 70,
        "Date": 100,
        "Cash": 80,
        "Credit": 80,
        "Total": 80
    }

    for col, width in column_settings.items():
        gross_profit_tree.heading(col, text=col.replace("ID", " ID"))
        gross_profit_tree.column(col, width=width, anchor="center")

    gross_profit_tree.heading("ProfitID", text="Profit ID")
    gross_profit_tree.heading("EmployeeID", text="Employee ID")
    gross_profit_tree.heading("StoreID", text="Store ID")
    gross_profit_tree.heading("Date", text="Date")
    gross_profit_tree.heading("Cash", text="Cash")
    gross_profit_tree.heading("Credit", text="Credit")
    gross_profit_tree.heading("Total", text="Total")
    gross_profit_tree.pack(fill="both", expand=True, padx=10, pady=10)

    # Load Gross Profit Button
    tk.Button(gross_profit_frame, text="Load Gross Profit", font=("Helvetica", 14),
              command=lambda: load_gross_profit(gross_profit_tree)).pack(pady=10)

def add_gross_profit(employee_id, store_id, date, cash, credit):
    """Adds a new gross profit record to the database."""
    if not employee_id or not store_id or not date or not cash or not credit:
        messagebox.showerror("Error", "All fields are required.")
        return
    try:
        query = """INSERT INTO Gross_Profit (Employee_ID, Store_ID, Date, Cash, Credit)
                   VALUES (%s, %s, %s, %s, %s)"""
        data = (int(employee_id), int(store_id), date, float(cash), float(credit))
        sqlConnector.connect(query, data)
        messagebox.showinfo("Success", "Gross profit added successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to add gross profit: {e}")

def load_gross_profit(tree):
    """Loads all gross profit records into the Treeview."""
    try:
        query = "SELECT * FROM Gross_Profit"
        results = sqlConnector.connect(query, ())
        # Clear existing rows
        for row in tree.get_children():
            tree.delete(row)
        # Insert new rows
        for result in results:
            tree.insert("", "end", values=result)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load gross profit: {e}")