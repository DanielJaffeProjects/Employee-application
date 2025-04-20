import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry  # Import DateEntry for date selection
from Main import sqlConnector


def create_bonus_tab(content_frame, tabs):
    """Creates the Bonus tab and adds it to the tabs dictionary."""
    bonus_frame = tk.Frame(content_frame, bg="white")
    bonus_frame.grid(row=0, column=0, sticky="nsew")
    tabs["Bonus"] = bonus_frame

    # Title
    tk.Label(bonus_frame, text="Manage Bonuses", font=("Helvetica", 18), bg="white").pack(pady=10)

    # Employee ID Dropdown
    tk.Label(bonus_frame, text="Employee ID:", font=("Helvetica", 14), bg="white").pack()
    emp_id_var = tk.StringVar()
    emp_id_dropdown = ttk.Combobox(bonus_frame, textvariable=emp_id_var, font=("Helvetica", 14))
    emp_id_dropdown.pack()
    load_employee_ids(emp_id_dropdown)

    # Bonus Rate
    tk.Label(bonus_frame, text="Bonus percent in decimal:", font=("Helvetica", 14), bg="white").pack()
    bonus_rate_entry = tk.Entry(bonus_frame, font=("Helvetica", 14))
    bonus_rate_entry.pack()

    # Rate Per Hour
    tk.Label(bonus_frame, text="Rate Per Hour:", font=("Helvetica", 14), bg="white").pack()
    rate_per_hour_entry = tk.Entry(bonus_frame, font=("Helvetica", 14))
    rate_per_hour_entry.pack()

    # Date
    tk.Label(bonus_frame, text="Date:", font=("Helvetica", 14), bg="white").pack()
    date_entry = DateEntry(bonus_frame, font=("Helvetica", 14), date_pattern="yyyy-mm-dd")
    date_entry.pack()

    # Submit Button
    tk.Button(bonus_frame, text="Add Bonus", font=("Helvetica", 14),
              command=lambda: add_employee_rate(emp_id_var.get(), bonus_rate_entry.get(),
                                               rate_per_hour_entry.get(), date_entry.get())).pack(pady=10)

    # Treeview for Displaying Employee Rates
    columns = ("EmpID", "Bonus_Rate", "Rate_Per_Hour", "Date", "Bonus_Amount Per Hour")
    rate_tree = ttk.Treeview(bonus_frame, columns=columns, show="headings")
    for col in columns:
        rate_tree.heading(col, text=col.replace("_", " "))
        rate_tree.column(col, width=120, anchor="center")
    rate_tree.pack(fill="both", expand=True, padx=10, pady=10)

    # Load Employee Rates Button
    tk.Button(bonus_frame, text="Load Employee Rates", font=("Helvetica", 14),
              command=lambda: load_employee_rates(rate_tree)).pack(pady=10)



def load_employee_ids(dropdown):
    """Loads Employee IDs into the dropdown."""
    try:
        query = "SELECT employee_id FROM Employee"
        results = sqlConnector.connect(query, ())
        dropdown["values"] = [row[0] for row in results]
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load Employee IDs: {e}")


def add_employee_rate(emp_id, bonus_rate, rate_per_hour, date):
    """Adds a new employee rate record to the Employee_Rate table."""
    if not emp_id:
        messagebox.showerror("Error", "Employee ID is required.")
        return

    # Validate inputs
    try:
        emp_id = int(emp_id)
        bonus_rate = float(bonus_rate) if bonus_rate else 0.00
        rate_per_hour = float(rate_per_hour) if rate_per_hour else 0.00
    except ValueError:
        messagebox.showerror("Error", "Please enter valid numeric values for the fields.")
        return

    try:
        query = """INSERT INTO Employee_Rate (employee_id, Bonus_Rate, Rate_Per_Hour, day_of_year)
                   VALUES (%s, %s, %s, %s)"""
        data = (emp_id, bonus_rate, rate_per_hour, date)
        sqlConnector.connect(query, data)
        messagebox.showinfo("Success", "Employee rate added successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to add employee rate: {e}")

def load_employee_rates(tree):
    """Loads all employee rate records into the Treeview."""
    try:
        query = "SELECT employee_id, Bonus_Rate, Rate_Per_Hour, day_of_year, bonus_amount FROM Employee_Rate"
        results = sqlConnector.connect(query, ())
        print(results)
        # Clear existing rows
        for row in tree.get_children():
            tree.delete(row)
        # Insert new rows
        for result in results:
            tree.insert("", "end", values=result)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load employee rates: {e}")