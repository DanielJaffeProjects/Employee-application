import tkinter as tk
from tkinter import ttk

from Main import sqlConnector
from Main.Notification import show_notification


def create_store_tab(content_frame, tabs, add_store_callback, delete_store_callback):
    """Creates the Store tab and adds it to the tabs dictionary."""
    store = tk.Frame(content_frame, bg="white")
    store.grid(row=0, column=0, sticky="nsew")
    tabs["Store"] = store

    # Add content to the store frame
    tk.Label(store, text="Manage Stores", font=("Helvetica", 18), bg="white").pack(pady=10)

    # Store Name Entry
    tk.Label(store, text="Store Name:", font=("Helvetica", 14), bg="white").pack()
    store_name_entry = tk.Entry(store, font=("Helvetica", 14))
    store_name_entry.pack()

    # Store Location Entry
    tk.Label(store, text="Store Location:", font=("Helvetica", 14), bg="white").pack()
    store_location_entry = tk.Entry(store, font=("Helvetica", 14))
    store_location_entry.pack()

    # Add Store Button
    tk.Button(store, text="Add Store", font=("Helvetica", 14),
              command=lambda: add_store(store_name_entry.get(), store_location_entry.get())).pack(pady=10)

    # Delete Store Button
    tk.Button(store, text="Delete Store", font=("Helvetica", 14),
              command=lambda: delete_store(store_name_entry.get())).pack(pady=10)


    # Store Records Section
    tk.Label(store, text="Store Records", font=("Helvetica", 14), bg="white").pack(pady=10)
    store_tree = ttk.Treeview(store, columns=("Name", "Location"), show="headings")
    store_tree.pack(fill="both", expand=True, padx=10, pady=5)

    # Define columns
    store_tree.heading("Name", text="Store Name")
    store_tree.heading("Location", text="Location")
    store_tree.column("Name", width=150, anchor="center")
    store_tree.column("Location", width=150, anchor="center")

    # Load Stores Button
    tk.Button(store, text="Load Stores", font=("Helvetica", 14),
              command=lambda: load_stores(store_tree)).pack(pady=10)

def add_store(store_name, store_location):
    """Adds a new store to the database."""
    if not store_name or not store_location:
        show_notification( "Both store name and location are required.")
        return
    try:
        # Check for duplicate store name
        query_check = "SELECT COUNT(*) FROM Store WHERE store_name = %s"
        data_check = (store_name,)
        result = sqlConnector.connect(query_check, data_check)
        if result[0][0] > 0:  # If the count is greater than 0, the store already exists
            show_notification(f"Store '{store_name}' already exists.")
            return

        # Insert the new store
        query_insert = "INSERT INTO Store (store_name, location) VALUES (%s, %s)"
        data_insert = (store_name, store_location)
        sqlConnector.connect(query_insert, data_insert)
        show_notification(f"Store '{store_name}' added successfully!")
    except Exception as e:
        show_notification(f"Failed to add store: {e}")

def delete_store(store_name):
    """Deletes a store from the database."""
    if not store_name:
        show_notification("Store name is required.")
        return
    try:
        query = "DELETE FROM Store WHERE store_name = %s"
        data = (store_name,)
        sqlConnector.connect(query, data)
        show_notification(f"Store '{store_name}' deleted successfully!")
    except Exception as e:
        show_notification(f"Failed to delete store: {e}")

def load_stores(store_tree):
    """Loads all stores from the database into the Treeview."""
    try:
        query = "SELECT store_name, location FROM Store"
        records = sqlConnector.connect(query, ())
        store_tree.delete(*store_tree.get_children())  # Clear existing records
        for record in records:
            store_tree.insert("", "end", values=record)
    except Exception as e:
        show_notification(f"Failed to load stores: {e}")