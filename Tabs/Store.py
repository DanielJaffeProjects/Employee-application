import tkinter as tk
from tkinter import messagebox

import sqlConnector


def create_store_tab(content_frame, tabs, add_store_callback, delete_store_callback):
    """Creates the Store tab and adds it to the tabs dictionary."""
    store = tk.Frame(content_frame, bg="white")
    store.grid(row=0, column=0, sticky="nsew")
    tabs["store"] = store

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

def add_store(store_name, store_location):
    """Adds a new store to the database."""
    if not store_name or not store_location:
        messagebox.showerror("Error", "Both store name and location are required.")
        return
    try:
        query = "INSERT INTO Store (store_name, location) VALUES (%s, %s)"
        data = (store_name, store_location)
        sqlConnector.connect(query, data)
        messagebox.showinfo("Success", f"Store '{store_name}' added successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to add store: {e}")

def delete_store(store_name):
    """Deletes a store from the database."""
    if not store_name:
        messagebox.showerror("Error", "Store name is required.")
        return
    try:
        query = "DELETE FROM Store WHERE store_name = %s"
        data = (store_name,)
        sqlConnector.connect(query, data)
        messagebox.showinfo("Success", f"Store '{store_name}' deleted successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to delete store: {e}")