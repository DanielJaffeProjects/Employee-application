import tkinter as tk
from tkinter import ttk

from Main import sqlConnector
from Main.Notification import show_notification
from Tabs.GenerateSummaryTable import generate_monthly_summary


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

        # Populate the combobox with store names
        self.store_data = self.get_store_data()
        self.store_combobox['values'] = [store['name'] for store in self.store_data]
        self.store_combobox.set("Select Store")

        tk.Label(input_frame, text="Month:", font=("Helvetica", 12), bg="white").grid(row=0, column=2, padx=5, pady=5)
        self.month_entry = tk.Entry(input_frame, font=("Helvetica", 12), width=5)
        self.month_entry.grid(row=0, column=3, padx=5, pady=5)

        tk.Label(input_frame, text="Year:", font=("Helvetica", 12), bg="white").grid(row=0, column=4, padx=5, pady=5)
        self.year_entry = tk.Entry(input_frame, font=("Helvetica", 12), width=5)
        self.year_entry.grid(row=0, column=5, padx=5, pady=5)

        # Vertical summary layout
        self.summary_frame = tk.Frame(self, bg="white")
        self.summary_frame.pack(pady=10)

        self.summary_labels = {}
        fields = [
            "Cash & Credit", "Total Expenses", "Total Merchandise", "Total Withdraw",
            "Total Payroll", "Net Profit", "Current Balance", "Actual Cash", "Actual Credit"
        ]
        for i, field in enumerate(fields):
            tk.Label(self.summary_frame, text=f"{field}:", font=("Helvetica", 12), bg="white").grid(row=i, column=0, sticky="w", padx=10, pady=5)
            value_label = tk.Label(self.summary_frame, text="0", font=("Helvetica", 12), bg="white", fg="black")
            value_label.grid(row=i, column=1, sticky="w", padx=10, pady=5)
            self.summary_labels[field] = value_label

        # Generate summary button
        generate_button = tk.Button(self, text="Generate Summary", font=("Helvetica", 14), bg="blue", fg="white",
                                     command=self.populate_summary)
        generate_button.pack(pady=10)

    def get_store_data(self):
        try:
            query = "SELECT store_id, store_name FROM store"
            result = sqlConnector.connect(query, ())
            return [{'id': row[0], 'name': row[1]} for row in result]
        except Exception as e:
            show_notification(f"Failed to fetch store data: {e}")
            return []

    def populate_summary(self):
        store_name = self.store_combobox.get()
        month = self.month_entry.get()
        year = self.year_entry.get()

        if store_name == "Select Store" or not month or not year:
            show_notification("Please select a Store Name, and enter Month and Year.")
            return

        if not month.isdigit() or not year.isdigit() or int(month) not in range(1, 13):
            show_notification("Month must be between 1 and 12, and Year must be numeric.")
            return

        store_id = next((store['id'] for store in self.store_data if store['name'] == store_name), None)
        if not store_id:
            show_notification("Invalid store selected.")
            return

        #generate a summary for that month
        generate_monthly_summary(store_id,month,year)

        # Fetch summary data
        query = """SELECT cash_and_credit, total_expenses, total_merchandise, total_withdraw,
                   total_payroll, net_profit, current_balance, actual_cash, actual_credit
                   FROM summary
                   WHERE store_id = %s AND month = %s AND year = %s"""
        try:
            result = sqlConnector.connect(query, (store_id, month, year))
            if result and isinstance(result, list) and len(result) > 0:
                values = result[0]
                for i, field in enumerate(self.summary_labels.keys()):
                    self.summary_labels[field].config(text=str(values[i]))
            else:
                # Reset all values to 0 if no data is found
                for field in self.summary_labels.keys():
                    self.summary_labels[field].config(text="0")
        except Exception as e:
            show_notification(f"Failed to fetch summary data: {e}")