import tkinter as tk
from tkinter import ttk, messagebox
from Main import sqlConnector


def create_bonus_tab(content_frame, tabs):
    """Creates the Bonus tab and adds it to the tabs dictionary."""
    bonus_frame = tk.Frame(content_frame, bg="white")
    bonus_frame.grid(row=0, column=0, sticky="nsew")
    tabs["Bonus"] = bonus_frame

    # Title
    tk.Label(bonus_frame, text="Manage Bonuses", font=("Helvetica", 18), bg="white").pack(pady=10)

    # Form Fields
    tk.Label(bonus_frame, text="Employee ID:", font=("Helvetica", 14), bg="white").pack()
    emp_id_entry = tk.Entry(bonus_frame, font=("Helvetica", 14))
    emp_id_entry.pack()

    tk.Label(bonus_frame, text="Bonus Amount:", font=("Helvetica", 14), bg="white").pack()
    bonus_amount_entry = tk.Entry(bonus_frame, font=("Helvetica", 14))
    bonus_amount_entry.pack()

    tk.Label(bonus_frame, text="Sales:", font=("Helvetica", 14), bg="white").pack()
    sales_entry = tk.Entry(bonus_frame, font=("Helvetica", 14))
    sales_entry.pack()

    tk.Label(bonus_frame, text="Gross:", font=("Helvetica", 14), bg="white").pack()
    gross_entry = tk.Entry(bonus_frame, font=("Helvetica", 14))
    gross_entry.pack()

    tk.Label(bonus_frame, text="Bonus Percentage:", font=("Helvetica", 14), bg="white").pack()
    bonus_percentage_entry = tk.Entry(bonus_frame, font=("Helvetica", 14))
    bonus_percentage_entry.pack()

    tk.Label(bonus_frame, text="Current Bonus Percentage:", font=("Helvetica", 14), bg="white").pack()
    current_bonus_percentage_entry = tk.Entry(bonus_frame, font=("Helvetica", 14))
    current_bonus_percentage_entry.pack()

    # Submit Button
    tk.Button(bonus_frame, text="Add Bonus", font=("Helvetica", 14),
              command=lambda: add_bonus(emp_id_entry.get(), bonus_amount_entry.get(), sales_entry.get(),
                                        gross_entry.get(), bonus_percentage_entry.get(),
                                        current_bonus_percentage_entry.get())).pack(pady=10)

    # Treeview for Displaying Bonuses
    columns = ("BonusID", "EmpID", "Bonus_Amount", "Sales", "Gross", "Bonus_Percentage", "Current_Bonus_Percentage")
    bonus_tree = ttk.Treeview(bonus_frame, columns=columns, show="headings")
    for col in columns:
        bonus_tree.heading(col, text=col)
        bonus_tree.column(col, width=120, anchor="center")
    bonus_tree.pack(fill="both", expand=True, padx=10, pady=10)

    # Load Bonuses Button
    tk.Button(bonus_frame, text="Load Bonuses", font=("Helvetica", 14),
              command=lambda: load_bonuses(bonus_tree)).pack(pady=10)

def add_bonus(emp_id, bonus_amount, sales, gross, bonus_percentage, current_bonus_percentage):
    """Adds a new bonus record to the database."""
    if not emp_id:
        messagebox.showerror("Error", "Employee ID is required.")
        return

    # Validate inputs
    try:
        emp_id = int(emp_id)
        bonus_amount = float(bonus_amount) if bonus_amount else 0.00
        sales = float(sales) if sales else 0.00
        gross = float(gross) if gross else 0.00
        bonus_percentage = float(bonus_percentage) if bonus_percentage else 0.00
        current_bonus_percentage = float(current_bonus_percentage) if current_bonus_percentage else 0.00
    except ValueError:
        messagebox.showerror("Error", "Please enter valid numeric values for the fields.")
        return

    # Check if Employee ID exists
    try:
        emp_check_query = "SELECT COUNT(*) FROM Employee WHERE employee_id = %s"
        emp_exists = sqlConnector.connect(emp_check_query, (emp_id,))
        if emp_exists[0][0] == 0:
            messagebox.showerror("Error", "Employee ID not found.")
            return
    except Exception as e:
        messagebox.showerror("Error", f"Failed to validate Employee ID: {e}")
        return

    try:
        query = """INSERT INTO Bonus (employee_id, Bonus_Amount, Sales, Gross, Bonus_Percentage, Current_Bonus_Percentage)
                   VALUES (%s, %s, %s, %s, %s, %s)"""
        data = (emp_id, bonus_amount or 0.00, sales or 0.00, gross or 0.00, bonus_percentage or 0.00,
                current_bonus_percentage or 0.00)
        sqlConnector.connect(query, data)
        messagebox.showinfo("Success", "Bonus added successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to add bonus: {e}")

def load_bonuses(tree):
    """Loads all bonus records into the Treeview."""
    try:
        query = "SELECT * FROM Bonus"
        results = sqlConnector.connect(query, ())
        # Clear existing rows
        for row in tree.get_children():
            tree.delete(row)
        # Insert new rows
        for result in results:
            tree.insert("", "end", values=result)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load bonuses: {e}")