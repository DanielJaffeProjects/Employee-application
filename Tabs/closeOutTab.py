# File: Main/closeOutTab.py
import tkinter as tk
from Main import sqlConnector
from Main.Notification import show_notification

BG_COLOR = "white"
LABEL_FONT = ("Helvetica", 18)

class CloseOutTab(tk.Frame):
    def __init__(self, parent, controller, selected_store):
        super().__init__(parent, bg=BG_COLOR)
        self.controller = controller
        self.selected_store = selected_store

        # Labels and input fields
        tk.Label(self, text="Enter credit", font=LABEL_FONT, bg=BG_COLOR).pack(pady=10)
        self.credit_entry = tk.Entry(self, font=LABEL_FONT)
        self.credit_entry.pack(pady=10)

        tk.Label(self, text="Enter cash in envelope", font=LABEL_FONT, bg=BG_COLOR).pack(pady=10)
        self.cash_entry = tk.Entry(self, font=LABEL_FONT)
        self.cash_entry.pack(pady=10)

        tk.Label(self, text="Enter expense", font=LABEL_FONT, bg=BG_COLOR).pack(pady=10)
        self.expense_entry = tk.Entry(self, font=LABEL_FONT)
        self.expense_entry.pack(pady=10)

        tk.Label(self, text="Comments", font=LABEL_FONT, bg=BG_COLOR).pack(pady=10)
        self.comments_entry = tk.Entry(self, font=LABEL_FONT)
        self.comments_entry.pack(pady=10)

        # Submit button
        submit_button = tk.Button(self, text="Submit", font=LABEL_FONT, command=self.submit_info)
        submit_button.pack(pady=20)

    def submit_info(self):
        credit = self.credit_entry.get()
        cash = self.cash_entry.get()
        expense = self.expense_entry.get()
        comments = self.comments_entry.get()
        store_name = self.selected_store.get()
        print(store_name)
        employee_id = self.controller.employee_id

        if not credit or not cash or not expense:
            show_notification("Please fill in all required fields (credit, cash, expense).")
            return

        try:
            credit_val = float(credit)
            cash_val = float(cash)
            expense_val = float(expense)
        except ValueError:
            show_notification("Credit, Cash, and Expense must be valid numbers.")
            return

        try:
            query = "SELECT firstName, lastName FROM employee WHERE employee_id = %s"
            result = sqlConnector.connect(query, (employee_id,))
            if not result:
                show_notification("Employee not found in database.")
                return
            first_name, last_name = result[0]
        except Exception as e:
            show_notification(f"Could not fetch employee info: {str(e)}")
            return

        try:
            # Fetch store_id based on store_name
            store_query = "SELECT store_id FROM store WHERE store_name = %s"
            store_result = sqlConnector.connect(store_query, (store_name,))
            if not store_result:
                show_notification("Store not found in database.")
                return
            store_id = store_result[0][0]

            # Check if a close-out entry already exists for the current date and store
            check_query = """SELECT * FROM employee_close 
                WHERE store_name = %s AND DATE(timestamp) = CURDATE()
            """
            existing_entry = sqlConnector.connect(check_query, (store_name,))
            print(existing_entry)

            if existing_entry:
                show_notification("A close-out entry for this store already exists for today.")
                return

            # Insert the new close-out entry
            insert_query = """
                INSERT INTO employee_close (
                    firstName, lastName, store_name, credit, cash_in_envelope, expense, comments, employee_id, store_id
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            data = (
            first_name, last_name, store_name, credit_val, cash_val, expense_val, comments, employee_id, store_id)
            sqlConnector.connect(insert_query, data)
            show_notification("Closing information submitted successfully.")

            self.credit_entry.delete(0, tk.END)
            self.cash_entry.delete(0, tk.END)
            self.expense_entry.delete(0, tk.END)
            self.comments_entry.delete(0, tk.END)

        except Exception as e:
            show_notification(f"An error occurred while submitting data: {str(e)}")