import tkinter as tk
from tkinter import ttk, messagebox
from Main import sqlConnector
from Main.Notification import show_notification

def create_payroll_tab(content_frame, tabs, _):
    payroll_frame = tk.Frame(content_frame, bg="white")
    payroll_frame.grid(row=0, column=0, sticky="nsew")
    tabs["Payroll"] = payroll_frame

    tk.Label(payroll_frame, text="Payroll", font=("Helvetica", 18), bg="white").pack(pady=10)

    # Employee Dropdown
    tk.Label(payroll_frame, text="Select Employee:", font=("Helvetica", 14), bg="white").pack()
    employee_combobox = ttk.Combobox(payroll_frame, font=("Helvetica", 14), state="readonly")
    employee_combobox.pack(pady=5)

    # Populate dropdown with employee names
    try:
        query = "SELECT employee_id, CONCAT(firstName, ' ', lastName) AS full_name FROM employee"
        employees = sqlConnector.connect(query, ())
        employee_data = {row[1]: row[0] for row in employees}
        employee_combobox["values"] = list(employee_data.keys())
    except Exception as e:
        show_notification(f"Failed to load employees: {e}")

    # Date Entry
    tk.Label(payroll_frame, text="Date (YYYY-MM-DD):", font=("Helvetica", 14), bg="white").pack()
    date_entry = tk.Entry(payroll_frame, font=("Helvetica", 14))
    date_entry.pack()

    # Hourly Rate Entry
    tk.Label(payroll_frame, text="Hourly Rate:", font=("Helvetica", 14), bg="white").pack()
    hourly_rate_entry = tk.Entry(payroll_frame, font=("Helvetica", 14))
    hourly_rate_entry.pack()

    # Hours Entry
    tk.Label(payroll_frame, text="Hours Worked:", font=("Helvetica", 14), bg="white").pack()
    hours_entry = tk.Entry(payroll_frame, font=("Helvetica", 14))
    hours_entry.pack()

    # Store Dropdown
    tk.Label(payroll_frame, text="Select Store:", font=("Helvetica", 14), bg="white").pack()
    store_combobox = ttk.Combobox(payroll_frame, font=("Helvetica", 14), state="readonly")
    store_combobox.pack(pady=5)

    # Populate dropdown with store names
    try:
        store_query = "SELECT store_id, store_name FROM Store"
        stores = sqlConnector.connect(store_query, ())
        store_data = {row[1]: row[0] for row in stores}
        store_combobox["values"] = list(store_data.keys())
    except Exception as e:
        show_notification(f"Failed to load stores: {e}")

    def handle_submit():
        employee_name = employee_combobox.get()
        store_name = store_combobox.get()

        if employee_name in employee_data and store_name in store_data:
            emp_id = employee_data[employee_name]
            store_id = store_data[store_name]
            submit_payroll(emp_id, store_id, date_entry.get(), hourly_rate_entry.get(), hours_entry.get())
        else:
            show_notification("Please select a valid employee and store.")

    tk.Button(payroll_frame, text="Submit Payroll", font=("Helvetica", 14),
              command=handle_submit).pack(pady=10)

    # Treeview for payroll records
    tk.Label(payroll_frame, text="Payroll Records", font=("Helvetica", 14), bg="white").pack(pady=10)
    payroll_tree = ttk.Treeview(
        payroll_frame,
        columns=("Employee ID", "Store ID", "Store Name", "Date", "Bonus Rate", "Hourly Rate", "Hours", "Amount",
                 "BonusAndAmount"),
        show="headings"
    )

    # Define columns
    for col in payroll_tree["columns"]:
        payroll_tree.heading(col, text=col)
        payroll_tree.column(col, anchor="center", width=120)

    payroll_tree.pack(pady=10)

    # Load Payroll Records Button
    def handle_load():
        name = employee_combobox.get()
        if name in employee_data:
            emp_id = employee_data[name]
            load_payroll_records(emp_id, payroll_tree)
        else:
            show_notification( "Please select a valid employee.")

    tk.Button(payroll_frame, text="Load Payroll Records", font=("Helvetica", 14),
              command=handle_load).pack(pady=10)


def submit_payroll(employee_id, store_id, date_str, hourly_rate, hours):
    if not store_id:
        show_notification("Store must be selected.")
        return

    try:
        # Validate date format
        from datetime import datetime
        datetime.strptime(date_str, "%Y-%m-%d")

        hourly_rate = float(hourly_rate)
        hours = float(hours)
        total_payment = hourly_rate * hours
        print("totalpayment", total_payment)

        # Check if a bonus exists for the employee
        bonus_check_query = """SELECT COUNT(*) FROM Employee_Rate WHERE employee_id = %s"""
        bonus_exists = sqlConnector.connect(bonus_check_query, (employee_id,))
        if bonus_exists[0][0] == 0:
            show_notification("A bonus must be added for this employee before processing payroll.")
            return

        # Fetch bonus rate
        bonus_query = """SELECT Bonus_Rate FROM Employee_Rate WHERE employee_id = %s"""
        result = sqlConnector.connect(bonus_query, (employee_id,))
        bonus_rate = float(result[0][0]) if result else 0.0
        bonus_amount = bonus_rate * hours
        total_with_bonus = total_payment + bonus_amount
        print("bonus_rate", bonus_rate)
        print("bonus_amount", bonus_amount)
        print("total_with_bonus", total_with_bonus)

        # Insert payroll record
        insert_query = """INSERT INTO Payroll (employee_id, store_id, timeofDate, hourly_rate, hours, total_payment, payment_with_bonus)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        sqlConnector.connect(insert_query, (employee_id, store_id, date_str, hourly_rate, hours, total_payment, total_with_bonus))
        show_notification("Payroll submitted successfully!")
    except ValueError:
        show_notification("Invalid input. Ensure all fields are filled correctly.")
    except Exception as e:
        show_notification(f"Failed to submit payroll: {str(e)}")

def load_payroll_records(employee_id, tree):
    try:
        tree.delete(*tree.get_children())
        query = """SELECT Payroll.employee_id, Payroll.store_id, Store.store_name, Payroll.timeofdate,
                   (SELECT Bonus_Rate FROM Employee_Rate
                    WHERE Employee_Rate.employee_id = Payroll.employee_id
                      AND Employee_Rate.day_of_year = Payroll.timeofdate) AS Bonus,
                   Payroll.hourly_rate, Payroll.hours, Payroll.total_payment, Payroll.payment_with_bonus
            FROM Payroll
            JOIN Store ON Payroll.store_id = Store.store_id
            WHERE Payroll.employee_id = %s
            ORDER BY Payroll.timeofDate DESC
        """

        records = sqlConnector.connect(query, (employee_id,))
        print(records)

        query = """SELECT Bonus_Rate
                   FROM Employee_Rate
                   WHERE employee_id = %s """
        Bonus_rate = sqlConnector.connect(query, (employee_id,))
        Bonus_rate = Bonus_rate[0][0]
        print(Bonus_rate)
        print(records)
        # put bonus rate into the second column if none
        updated_records = []
        for row in records:
            row = list(row)  # Convert tuple to list
            if row[4] is None:  # Check if the fifth element (Bonus) is None
                row[4] = Bonus_rate  # Replace None with Bonus_Rate
            updated_records.append(tuple(row))  # Convert back to tuple if needed

        print(updated_records)
        for row in updated_records:
            tree.insert("", "end", values=row)
    except Exception as e:
        show_notification( f"Could not load payroll records: {str(e)}")