import tkinter as tk
from tkinter import ttk

from Main import sqlConnector
from Main.Notification import show_notification


class SummaryTab(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg="white")

        # Title Label
        title_label = tk.Label(self, text="Monthly Summary", font=("Helvetica", 16), bg="white", fg="black")
        title_label.pack(pady=10)

        # Input fields for store, month, and year
        input_frame = tk.Frame(self, bg="white")
        input_frame.pack(pady=10)

        tk.Label(input_frame, text="Store Name:", font=("Helvetica", 12), bg="white").grid(row=0, column=0, padx=5, pady=5)
        self.store_combobox = ttk.Combobox(input_frame, font=("Helvetica", 12), width=20, state="readonly")
        self.store_combobox.grid(row=0, column=1, padx=5, pady=5)

        # Populate the combobox with store names (replace with actual database query)
        self.store_data = self.get_store_data()
        self.store_combobox['values'] = [store['name'] for store in self.store_data]
        self.store_combobox.set("Select Store")  # Default placeholder

        tk.Label(input_frame, text="Month:", font=("Helvetica", 12), bg="white").grid(row=0, column=2, padx=5, pady=5)
        self.month_entry = tk.Entry(input_frame, font=("Helvetica", 12), width=5)
        self.month_entry.grid(row=0, column=3, padx=5, pady=5)

        tk.Label(input_frame, text="Year:", font=("Helvetica", 12), bg="white").grid(row=0, column=4, padx=5, pady=5)
        self.year_entry = tk.Entry(input_frame, font=("Helvetica", 12), width=5)
        self.year_entry.grid(row=0, column=5, padx=5, pady=5)

        # Treeview for displaying summary data
        self.tree = ttk.Treeview(self, columns=(
            "Employee ID", "Store ID", "Cash & Credit", "Total Expenses", "Total Merchandise",
            "Total Withdraw", "Total Payroll", "Net Profit", "Current Balance", "Actual Cash", "Actual Credit"
        ), show="headings", height=15)
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        # Define column headings
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor="center")

        # Generate summary button
        generate_button = tk.Button(self, text="Generate Summary", font=("Helvetica", 14), bg="blue", fg="white",
                                     command=self.populate_summary)
        generate_button.pack(pady=10)

    def get_store_data(self):
        # Mocked store data, replace with a database query to fetch actual store names and IDs
        try:
            query = "SELECT store_id, store_name FROM store"
            result = sqlConnector.connect(query, ())
            return [{'id': row[0], 'name': row[1]} for row in result]
        except Exception as e:
            show_notification( f"Failed to fetch store data: {e}")
            return []

    def populate_summary(self):
        # Get the store name, month, and year from the input fields
        store_name = self.store_combobox.get()
        month = self.month_entry.get()
        year = self.year_entry.get()

        # Validate inputs
        if store_name == "Select Store" or not month or not year:
            show_notification("Please select a Store Name, and enter Month and Year.")
            return

        if not month.isdigit() or not year.isdigit() or int(month) not in range(1, 13):
            show_notification( "Month must be between 1 and 12, and Year must be numeric.")
            return

        # Get the store ID from the selected store name
        store_id = next((store['id'] for store in self.store_data if store['name'] == store_name), None)
        if not store_id:
            show_notification("Invalid store selected.")
            return

        # Clear existing data
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Call the generate_monthly_summary function with the specified inputs
        self.generate_monthly_summary(store_id, month, year)

        # Fetch the summary data
        query = "SELECT * FROM summary WHERE store_id = %s AND MONTH(date) = %s AND YEAR(date) = %s"
        try:
            result = sqlConnector.connect(query, (store_id, month, year))
            if not result or not isinstance(result, list):  # Check if result is valid
                show_notification( "No data found for the specified store, month, and year.")
                return

            # Populate the Treeview with the fetched data
            for row in result:
                self.tree.insert("", "end", values=row)
        except Exception as e:
            show_notification("Failed to fetch summary data: {e}")

    def generate_monthly_summary(self, store_id, month, year):
        print("generating summary")
        if not store_id or not month or not year:
            show_notification("Store ID, month, and year are required.")
            return

        # try:
        #     # Query to calculate the summary for the given store, month, and year
        #     query = """
        #         SELECT
        #             store_id,
        #             SUM(reg_in + reg_out) AS cash_and_credit,
        #             SUM(expense) AS total_expenses,
        #             SUM(Merch_Value) AS total_merchandise,
        #             SUM(amount) AS total_withdraw,
        #             SUM(hours * hourly_rate + bonus) AS total_payroll,
        #             (SUM(reg_in + reg_out) - SUM(expense) - SUM(Merch_Value) - SUM(amount) - SUM(hours * hourly_rate + bonus)) AS net_profit,
        #             SUM(reg_in + reg_out) AS current_balance,
        #             SUM(reg_in) AS actual_cash,
        #             SUM(reg_out) AS actual_credit
        #         FROM
        #             clockTable
        #         LEFT JOIN Expense ON clockTable.employee_id = Expense.employee_id AND clockTable.store_id = Expense.store_id
        #         LEFT JOIN Merchandise ON clockTable.store_id = Merchandise.StoreID
        #         LEFT JOIN withdraw ON clockTable.employee_id = withdraw.employee_id AND clockTable.store_id = withdraw.store_id
        #         LEFT JOIN Payroll ON clockTable.employee_id = Payroll.employee_id
        #         WHERE
        #             clockTable.store_id = %s AND MONTH(clock_in) = %s AND YEAR(clock_in) = %s
        #         GROUP BY
        #             employee_id, store_id
        #     """
        #     data = (store_id, month, year)
        #     result = sqlConnector.connect(query, data)
        #
        #     if not result:
        #         messagebox.showinfo("Notification", "No data found for the specified store, month, and year.")
        #         return
        #
        #     # Insert the summary into the summary table
        #     insert_query = """
        #         INSERT INTO summary (
        #             employee_id, store_id, cash_and_credit, total_expenses, total_merchandise,
        #             total_withdraw, total_payroll, net_profit, current_balance, actual_cash, actual_credit
        #         ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        #     """
        #     for row in result:
        #         sqlConnector.connect(insert_query, row)
        #
        #     messagebox.showinfo("Notification", "Monthly summary generated successfully.")
        #
        # except Exception as e:
        #     messagebox.showinfo("Notification", f"An error occurred: {str(e)}")