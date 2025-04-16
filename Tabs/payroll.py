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


def submit_payroll(employee_id, date, bonus, hourly_rate, hours):
    """Submits payroll data to the database."""
    if not employee_id or not date or not bonus or not hourly_rate or not hours:
        messagebox.showerror("Error", "All fields must be filled out.")
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
