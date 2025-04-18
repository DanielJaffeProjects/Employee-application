import tkinter as tk
from datetime import datetime
from tkinter import messagebox
from tkinter import ttk
import re
import sqlConnector


# -------------------------------
# Enter Invoice Tab (as provided)
# -------------------------------
def createInvoice(content_frame,tabs):
    enter_invoice_frame = tk.Frame(content_frame, bg="white")
    enter_invoice_frame.grid(row=0, column=0, sticky="nsew")
    tk.Label(enter_invoice_frame, text="Enter Invoice", font=("Helvetica", 18), bg="white").pack(pady=10)

    tk.Label(enter_invoice_frame, text="Invoice ID:", font=("Helvetica", 14), bg="white").pack()
    invoice_id = tk.Entry(enter_invoice_frame, font=("Helvetica", 14))
    invoice_id.pack()

    tk.Label(enter_invoice_frame, text="Company:", font=("Helvetica", 14), bg="white").pack()
    invoice_company = tk.Entry(enter_invoice_frame, font=("Helvetica", 14))
    invoice_company.pack()

    tk.Label(enter_invoice_frame, text="Amount:", font=("Helvetica", 14), bg="white").pack()
    invoice_amount = tk.Entry(enter_invoice_frame, font=("Helvetica", 14))
    invoice_amount.pack()

    tk.Label(enter_invoice_frame, text="Date received: ", font=("Helvetica", 14), bg="white").pack()
    date_received = tk.Entry(enter_invoice_frame, font=("Helvetica", 14))
    date_received.pack()

    tk.Label(enter_invoice_frame, text="Date Due:", font=("Helvetica", 14), bg="white").pack()
    date_due = tk.Entry(enter_invoice_frame, font=("Helvetica", 14))
    date_due.pack()

    # Replace the "Paid (Yes/No):" Entry with Radiobuttons
    tk.Label(enter_invoice_frame, text="Paid Status:", font=("Helvetica", 14), bg="white").pack()

    # Variable to store the selected paid status
    invoice_paid_status = tk.StringVar(value="unpaid")  # Default to "unpaid"

    # Radiobuttons for "Paid" and "Unpaid"
    paid_button = tk.Radiobutton(enter_invoice_frame, text="Paid", variable=invoice_paid_status, value="paid",
                                 font=("Helvetica", 14), bg="white")
    paid_button.pack()

    unpaid_button = tk.Radiobutton(enter_invoice_frame, text="Unpaid", variable=invoice_paid_status, value="unpaid",
                                   font=("Helvetica", 14), bg="white")
    unpaid_button.pack()

    tk.Button(enter_invoice_frame, text="Submit Invoice", font=("Helvetica", 14),
              command=lambda: submit_invoice(invoice_id.get(), invoice_company.get(), invoice_amount.get(),
                                                  date_received.get(), date_due.get(),
                                                  invoice_paid_status.get())).pack(pady=10)

    tk.Button(enter_invoice_frame, text="Update Invoice", font=("Helvetica", 14),
              command=lambda: update_invoice(invoice_id.get(), invoice_company.get(), invoice_amount.get(),
                                             date_received.get(), date_due.get(), invoice_paid_status.get())).pack(pady=10)
    # Invoice Records Treeview
    tk.Label(enter_invoice_frame, text="Invoice Records", font=("Helvetica", 14), bg="white").pack(pady=10)
    invoice_tree = ttk.Treeview(enter_invoice_frame, columns=("ID", "Company", "Amount", "Received", "Due", "Paid"), show="headings",height = 5)
    invoice_tree.pack(fill="both", expand=True, padx=10, pady=5)

    # Define columns
    invoice_tree.heading("ID", text="Invoice ID")
    invoice_tree.heading("Company", text="Company")
    invoice_tree.heading("Amount", text="Amount")
    invoice_tree.heading("Received", text="Date Received")
    invoice_tree.heading("Due", text="Date Due")
    invoice_tree.heading("Paid", text="Paid Status")

    invoice_tree.column("ID", width=100, anchor="center")
    invoice_tree.column("Company", width=150, anchor="center")
    invoice_tree.column("Amount", width=100, anchor="center")
    invoice_tree.column("Received", width=120, anchor="center")
    invoice_tree.column("Due", width=120, anchor="center")
    invoice_tree.column("Paid", width=100, anchor="center")

    # Load Invoice Records Button
    tk.Button(enter_invoice_frame, text="Load Invoice Records", font=("Helvetica", 14),
              command=lambda: load_invoice_records(invoice_tree)).pack(pady=10)



    tabs["Enter Invoice"] = enter_invoice_frame


def submit_invoice(invoice_id, invoice_company, invoice_amount, date_received, date_due, invoice_paid):
    if not invoice_id or not invoice_company or not invoice_amount or not date_received or not date_due or not invoice_paid:
        messagebox.showerror("Error", "All fields must be filled out.")
        return

    # Validate Invoice ID
    if not re.match(r"^[a-zA-Z0-9]+$", invoice_id):
        messagebox.showerror("Error", "Invoice ID must be alphanumeric.")
        return

    # Check for duplicate Invoice ID
    try:
        query = "SELECT COUNT(*) FROM Invoice WHERE invoice_id = %s"
        result = sqlConnector.connect(query, (invoice_id,))
        if result[0][0] > 0:
            messagebox.showerror("Error", f"Invoice ID '{invoice_id}' already exists.")
            return
    except Exception as e:
        messagebox.showerror("Error", f"Failed to check for duplicate Invoice ID: {e}")
        return

    # Validate Invoice Amount
    try:
        invoice_amount = float(invoice_amount)
        if invoice_amount <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Error", "Invoice Amount must be a positive number.")
        return

    # Validate Dates
    try:
        datetime.strptime(date_received, "%Y-%m-%d")
        datetime.strptime(date_due, "%Y-%m-%d")
    except ValueError:
        messagebox.showerror("Error", "Dates must be in the format YYYY-MM-DD and valid.")
        return

    try:
           # SQL query to insert invoice data
        query = """
          INSERT INTO Invoice (invoice_id, invoice_company, invoice_amount, date_received, date_due, invoice_paid)
          VALUES (%s, %s, %s, %s, %s, %s)
          """
        data = (invoice_id, invoice_company, invoice_amount, date_received, date_due, invoice_paid)

        # Execute the query
        sqlConnector.connect(query, data)

        messagebox.showinfo("Success", f"Invoice {invoice_id} submitted successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to submit invoice: {e}")

def load_invoice_records(invoice_tree):
    """Loads invoice records into the Treeview."""
    try:
        query = "SELECT invoice_id, invoice_company, invoice_amount, date_received, date_due, invoice_paid FROM Invoice"
        data = ()
        records = sqlConnector.connect(query,(data))
        invoice_tree.delete(*invoice_tree.get_children())  # Clear existing records
        for record in records:
            invoice_tree.insert("", "end", values=record)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load invoice records: {e}")

def update_invoice(invoice_id, invoice_company, invoice_amount, date_received, date_due, invoice_paid):
    """Updates the selected invoice in the database."""
    if not invoice_id or not invoice_company or not invoice_amount or not date_received or not date_due or not invoice_paid:
        messagebox.showerror("Error", "All fields must be filled out.")
        return

    try:
        invoice_amount = float(invoice_amount)
        if invoice_amount <= 0:
            raise ValueError
        datetime.strptime(date_received, "%Y-%m-%d")
        datetime.strptime(date_due, "%Y-%m-%d")
    except ValueError:
        messagebox.showerror("Error", "Invalid input. Check the amount and date formats.")
        return

    try:
        query = """
        UPDATE Invoice
        SET invoice_company = %s, invoice_amount = %s, date_received = %s, date_due = %s, invoice_paid = %s
        WHERE invoice_id = %s
        """
        data = (invoice_company, invoice_amount, date_received, date_due, invoice_paid, invoice_id)
        sqlConnector.connect(query, data)
        messagebox.showinfo("Success", f"Invoice {invoice_id} updated successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to update invoice: {e}")