import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

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

    tabs["Enter Invoice"] = enter_invoice_frame


def submit_invoice(invoice_id, invoice_company, invoice_amount, date_received, date_due, invoice_paid):
    if not invoice_id or not invoice_company or not invoice_amount or not date_received or not date_due or not invoice_paid:
        messagebox.showerror("Error", "All fields must be filled out.")
        return

    try:
        # Convert paid status to match ENUM values in the database
        paid_status = "paid" if invoice_paid.lower() == "yes" else "unpaid"

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