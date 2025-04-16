import tkinter as tk
from tkinter import messagebox
import sqlConnector

def create_merchandise_tab(content_frame, tabs):
    # Create Merchandise Tab
    enter_merch_frame = tk.Frame(content_frame, bg="white")
    enter_merch_frame.grid(row=0, column=0, sticky="nsew")
    tk.Label(enter_merch_frame, text="Enter Merchandise", font=("Helvetica", 18), bg="white").pack(pady=10)

    # Merchandise Type
    tk.Label(enter_merch_frame, text="Merchandise Type:", font=("Helvetica", 14), bg="white").pack()
    merch_type = tk.Entry(enter_merch_frame, font=("Helvetica", 14))
    merch_type.pack()

    # Merchandise Value
    tk.Label(enter_merch_frame, text="Merchandise Value:", font=("Helvetica", 14), bg="white").pack()
    merch_value = tk.Entry(enter_merch_frame, font=("Helvetica", 14))
    merch_value.pack()

    # Purchase Date
    tk.Label(enter_merch_frame, text="Purchase Date (YYYY-MM-DD):", font=("Helvetica", 14), bg="white").pack()
    purchase_date = tk.Entry(enter_merch_frame, font=("Helvetica", 14))
    purchase_date.pack()

    # Store ID
    tk.Label(enter_merch_frame, text="Store ID:", font=("Helvetica", 14), bg="white").pack()
    store_id = tk.Entry(enter_merch_frame, font=("Helvetica", 14))
    store_id.pack()

    # Submit Button
    tk.Button(enter_merch_frame, text="Submit Merchandise", font=("Helvetica", 14),
              command=lambda: submit_merchandise(merch_type.get(), merch_value.get(), purchase_date.get(),
                                                 store_id.get())).pack(pady=10)
    tabs["Enter Merchandise"] = enter_merch_frame

def submit_merchandise(merch_type, merch_value, purchase_date, store_id):
    if not merch_type or not merch_value or not purchase_date:
        messagebox.showerror("Error", "All fields except Store ID must be filled out.")
        return

    try:
        # SQL query to insert merchandise data
        query = """
        INSERT INTO Merchandise (Merch_Type, Merch_Value, Purchase_Date, StoreID)
        VALUES (%s, %s, %s, %s)
        """
        data = (merch_type, float(merch_value), purchase_date, store_id)

        # Execute the query
        sqlConnector.connect(query, data)

        messagebox.showinfo("Success", "Merchandise added successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to add merchandise: {e}")