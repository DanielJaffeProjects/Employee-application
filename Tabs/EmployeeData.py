import tkinter as tk
from tkinter import ttk, messagebox
from Main import sqlConnector


def create_employee_history_tab(content_frame, tabs, days):
    """Creates the Employee History tab with two tables."""
    history_frame = tk.Frame(content_frame, bg="white")
    history_frame.grid(row=0, column=0, sticky="nsew")
    tabs["Employee History"] = history_frame

    # Title
    tk.Label(history_frame, text="Employee History", font=("Helvetica", 18), bg="white").pack(pady=10)

    # Employee ID Input
    tk.Label(history_frame, text="Enter Employee ID:", font=("Helvetica", 14), bg="white").pack(pady=5)
    employee_id_entry = tk.Entry(history_frame, font=("Helvetica", 14))
    employee_id_entry.pack(pady=5)

    # Clock-In/Clock-Out Table
    tk.Label(history_frame, text="Clock-In/Clock-Out Records", font=("Helvetica", 14), bg="white").pack(pady=5)
    clock_tree = ttk.Treeview(history_frame, columns=("ClockID", "ClockIn", "ClockOut", "RegIn", "RegOut", "Duration"), show="headings")
    clock_tree.pack(fill="both", expand=True, padx=10, pady=5)

    # Define columns for Clock-In/Clock-Out table
    clock_columns = {
        "ClockID": 70,
        "ClockIn": 150,
        "ClockOut": 150,
        "RegIn": 100,
        "RegOut": 100,
        "Duration": 100
    }
    for col, width in clock_columns.items():
        clock_tree.heading(col, text=col)
        clock_tree.column(col, width=width, anchor="center")

    # Close-Out Table
    tk.Label(history_frame, text="Close-Out Records", font=("Helvetica", 14), bg="white").pack(pady=5)
    close_tree = ttk.Treeview(history_frame, columns=("CloseID", "StoreName", "Credit", "Cash", "Expense", "Comments"), show="headings")
    close_tree.pack(fill="both", expand=True, padx=10, pady=5)

    # Define columns for Close-Out table
    close_columns = {
        "CloseID": 70,
        "StoreName": 150,
        "Credit": 100,
        "Cash": 100,
        "Expense": 100,
        "Comments": 200
    }
    for col, width in close_columns.items():
        close_tree.heading(col, text=col)
        close_tree.column(col, width=width, anchor="center")

    # Load Data Button
    def on_load_history():
        employee_id = employee_id_entry.get()
        if not employee_id.isdigit():
            messagebox.showerror("Error", "Please enter a valid Employee ID.")
            return
        load_employee_history(clock_tree, close_tree, int(employee_id), days)

    tk.Button(history_frame, text="Load History", font=("Helvetica", 14), bg="#4CAF50", fg="white",
              command=on_load_history).pack(pady=10)


def load_employee_history(clock_tree, close_tree, employee_id, days):
    """Loads employee history data for the last `days` days for a specific employee into the tables."""
    print(f"Loading employee history for Employee ID: {employee_id}...")
    try:
        # Check if the Employee ID exists in the database
        validation_query = "SELECT COUNT(*) FROM employee WHERE employee_id = %s"
        result = sqlConnector.connect(validation_query, (int(employee_id),))
        if result[0][0] == 0:
            messagebox.showerror("Error", "Employee ID does not exist.")
            return
    except Exception as e:
        messagebox.showerror("Error", f"Failed to validate Employee ID: {e}")

    try:
        # Fetch Clock-In/Clock-Out Records
        clock_query = """SELECT clock_id, clock_in, clock_out, reg_in, reg_out, duration
            FROM clockTable
            WHERE employee_id = %s AND clock_in >= DATE_SUB(CURDATE(), INTERVAL %s DAY)
        """

        clock_data = sqlConnector.connect(clock_query, (employee_id, days))
        print(f"Clock Data: {clock_data}")

        # Populate the Clock-In/Clock-Out table
        clock_tree.delete(*clock_tree.get_children())
        for row in clock_data:
            clock_tree.insert("", "end", values=row)

        # Fetch Close-Out Records
        close_query = """SELECT close_id, store_name, credit, cash_in_envelope, expense, comments
            FROM employee_close
            WHERE employee_id = %s AND timestamp >= DATE_SUB(CURDATE(), INTERVAL %s DAY)
        """
        close_data = sqlConnector.connect(close_query, (employee_id, days))
        print(f"Close Data: {close_data}")

        # Populate the Close-Out table
        close_tree.delete(*close_tree.get_children())
        for row in close_data:
            close_tree.insert("", "end", values=row)

        messagebox.showinfo("Success", f"Employee history for Employee ID {employee_id} for the last {days} days loaded successfully.")
    except Exception as e:
        print(f"Error loading employee history: {e}")
        messagebox.showerror("Error", f"Failed to load employee history: {e}")