import tkinter as tk
from tkinter import ttk, messagebox
import sqlConnector

def create_payroll_tab(content_frame, tabs,employee_id):
    """Creates the Payroll tab and adds it to the tabs dictionary."""
    payroll_frame = tk.Frame(content_frame, bg="white")
    payroll_frame.grid(row=0, column=0, sticky="nsew")
    tabs["Payroll"] = payroll_frame

    tk.Label(payroll_frame, text="Payroll", font=("Helvetica", 18), bg="white").pack(pady=10)

    # Date Entry
    tk.Label(payroll_frame, text="Date (YYYY-MM-DD):", font=("Helvetica", 14), bg="white").pack()
    date_entry = tk.Entry(payroll_frame, font=("Helvetica", 14))
    date_entry.pack()

    # Bonus Entry
    tk.Label(payroll_frame, text="Bonus:", font=("Helvetica", 14), bg="white").pack()
    bonus_entry = tk.Entry(payroll_frame, font=("Helvetica", 14))
    bonus_entry.pack()

    # Hourly Rate Entry
    tk.Label(payroll_frame, text="Hourly Rate:", font=("Helvetica", 14), bg="white").pack()
    hourly_rate_entry = tk.Entry(payroll_frame, font=("Helvetica", 14))
    hourly_rate_entry.pack()

    # Hours Entry
    tk.Label(payroll_frame, text="Hours Worked:", font=("Helvetica", 14), bg="white").pack()
    hours_entry = tk.Entry(payroll_frame, font=("Helvetica", 14))
    hours_entry.pack()

    # Submit Button
    tk.Button(payroll_frame, text="Submit Payroll", font=("Helvetica", 14),
              command=lambda: submit_payroll(employee_id,date_entry.get(), bonus_entry.get(),
                                             hourly_rate_entry.get(), hours_entry.get())).pack(pady=10)

  # Payroll Records Treeview
    tk.Label(payroll_frame, text="Payroll Records", font=("Helvetica", 14), bg="white").pack(pady=10)
    payroll_tree = ttk.Treeview(payroll_frame, columns=("Date", "Bonus", "Hourly Rate", "Hours"), show="headings")
    payroll_tree.pack(fill="both", expand=True, padx=10, pady=5)

    # Define columns
    payroll_tree.heading("Date", text="Date")
    payroll_tree.heading("Bonus", text="Bonus")
    payroll_tree.heading("Hourly Rate", text="Hourly Rate")
    payroll_tree.heading("Hours", text="Hours")

    payroll_tree.column("Date", width=100, anchor="center")
    payroll_tree.column("Bonus", width=100, anchor="center")
    payroll_tree.column("Hourly Rate", width=100, anchor="center")
    payroll_tree.column("Hours", width=100, anchor="center")

    # Load Payroll Records Button
    tk.Button(payroll_frame, text="Load Payroll Records", font=("Helvetica", 14),
              command=lambda: load_payroll_records(employee_id, payroll_tree)).pack(pady=10)

def submit_payroll(employee_id, date, bonus, hourly_rate, hours):
    """Submits payroll data to the database."""
    if not employee_id or not date or not bonus or not hourly_rate or not hours:
        messagebox.showerror("Error", "All fields must be filled out.")
        return

    # Validate input values
    try:
        # Validate employee_id
        employee_id = int(employee_id)
        if employee_id <= 0:
            raise ValueError("Employee ID must be a positive integer.")

        # Validate date format
        from datetime import datetime
        datetime.strptime(date, "%Y-%m-%d")  # Raises ValueError if the format is incorrect

        # Validate bonus, hourly_rate, and hours
        bonus = float(bonus)
        hourly_rate = float(hourly_rate)
        hours = int(hours)

        if bonus < 0 or hourly_rate < 0 or hours < 0:
            raise ValueError("Bonus, Hourly Rate, and Hours must be non-negative values.")
    except ValueError as ve:
        messagebox.showerror("Input Error", f"Invalid input: {ve}")
        return

    try:
        query = """
        INSERT INTO Payroll (employee_id, date, bonus, hourly_rate, hours)
        VALUES (%s, %s, %s, %s, %s)
        """
        data = (int(employee_id), date, float(bonus), float(hourly_rate), int(hours))
        sqlConnector.connect(query, data)
        messagebox.showinfo("Success", "Payroll record added successfully!")
    except Exception as e:
        messagebox.showerror("Database Error", f"An error occurred: {str(e)}")


def load_payroll_records(employee_id, payroll_tree):
    """Loads payroll records for the given employee into the Treeview."""
    try:
        query = "SELECT date, bonus, hourly_rate, hours FROM Payroll WHERE employee_id = %s"
        records = sqlConnector.connect(query, (employee_id,))
        payroll_tree.delete(*payroll_tree.get_children())  # Clear existing records
        for record in records:
            payroll_tree.insert("", "end", values=record)
    except Exception as e:
        messagebox.showerror("Database Error", f"An error occurred: {str(e)}")