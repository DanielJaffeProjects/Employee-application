import tkinter as tk
from tkinter import messagebox, simpledialog
from manageEmployees import ManageEmployees
import sqlConnector

class OwnerPage(ManageEmployees):
    def __init__(self, parent, controller):
        super().__init__(parent,controller)
        self.controller = controller
        self.configure(bg="white")

        # Top frame for store selection dropdown
        top_frame = tk.Frame(self, bg="white", bd=1, relief="solid")
        top_frame.pack(side="top", fill="x", padx=10, pady=10)

        # Centered label (ALOHA)
        aloha_label = tk.Label(top_frame, text="ALOHA", font=("Helvetica", 14), bg="white", fg="black")
        aloha_label.place(relx=0.5, rely=0.5, anchor="center")

        # Right label (name of employee)
        tk.Label(top_frame, text="Name of employee", font=("Helvetica", 14), bg="white", fg="black").pack(side="right",
                                                                                                          padx=(5, 10))

        # Store Selection Dropdown
        selected_store = tk.StringVar()
        selected_store.set("Select Store")

        # Create Main Layout
        main_frame = tk.Frame(self, bg="white")
        main_frame.pack(fill="both", expand=True)

        # Left Panel for Tabs
        tab_frame = tk.Frame(main_frame, bg="white", width=250, bd=1, relief="solid")
        tab_frame.pack(side="left", fill="y", padx=10, pady=10)

        # Right Panel for Content
        content_frame = tk.Frame(main_frame, bg="white", bd=1, relief="solid")
        content_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        content_frame.grid_rowconfigure(0, weight=1)
        content_frame.grid_columnconfigure(0, weight=1)

        # Dictionary to hold the tabs
        tabs = {}

        # -------------------------------
        # Add Store Tab
        # -------------------------------
        add_store_frame = tk.Frame(content_frame, bg="white")
        add_store_frame.grid(row=0, column=0, sticky="nsew")
        tabs["Add Store"] = add_store_frame

        tk.Label(add_store_frame, text="Add Store", font=("Helvetica", 18), bg="white").pack(pady=10)

        tk.Label(add_store_frame, text="Store Name:", font=("Helvetica", 14), bg="white").pack()
        store_name = tk.Entry(add_store_frame, font=("Helvetica", 14))
        store_name.pack()

        tk.Label(add_store_frame, text="Store Location:", font=("Helvetica", 14), bg="white").pack()
        store_location = tk.Entry(add_store_frame, font=("Helvetica", 14))
        store_location.pack()

        tk.Button(add_store_frame, text="Add Store", font=("Helvetica", 14),
                  command=lambda: self.add_store(store_name.get(), store_location.get())).pack(pady=10)

        # -------------------------------
        # Manage Stores Tab
        # -------------------------------
        manage_stores_frame = tk.Frame(content_frame, bg="white")
        manage_stores_frame.grid(row=0, column=0, sticky="nsew")
        tabs["Manage Stores"] = manage_stores_frame

        tk.Label(manage_stores_frame, text="Manage Stores", font=("Helvetica", 18), bg="white").pack(pady=10)

        # Dropdown to select store to edit/delete
        tk.Label(manage_stores_frame, text="Select Store:", font=("Helvetica", 14), bg="white").pack()
        selected_edit_store = tk.StringVar()
        store_edit_dropdown = tk.OptionMenu(manage_stores_frame, selected_edit_store, "")
        store_edit_dropdown.config(font=("Helvetica", 14), bg="white")
        store_edit_dropdown.pack(pady=5)

        # Edit Store Fields
        tk.Label(manage_stores_frame, text="New Store Name:", font=("Helvetica", 14), bg="white").pack()
        new_store_name = tk.Entry(manage_stores_frame, font=("Helvetica", 14))
        new_store_name.pack()

        tk.Label(manage_stores_frame, text="New Store Location:", font=("Helvetica", 14), bg="white").pack()
        new_store_location = tk.Entry(manage_stores_frame, font=("Helvetica", 14))
        new_store_location.pack()

        tk.Button(manage_stores_frame, text="Update Store", font=("Helvetica", 14),
                  command=lambda: self.update_store(
                      selected_edit_store.get(),
                      new_store_name.get(),
                      new_store_location.get()
                  )).pack(pady=10)

        tk.Button(manage_stores_frame, text="Delete Store", font=("Helvetica", 14),
                  command=lambda: self.delete_store(selected_edit_store.get())).pack(pady=5)

        # -------------------------------
        # Function to Show Selected Tab
        # -------------------------------
        def show_tab(tab_name):
            tabs[tab_name].tkraise()

        for title in tabs:
            btn = tk.Button(tab_frame, text=title, font=("Helvetica", 14), fg="black", bg="white",
                            relief="solid", bd=2, command=lambda t=title: show_tab(t), width=25, height=2)
            btn.pack(pady=5, padx=10, fill="x")

        # Show the default tab
        show_tab("Add Store")

        # Create bottom frame for logout
        self.create_bottom_frame()

        # Populate store dropdown
        self.populate_store_dropdowns()

    def create_bottom_frame(self):
        """Creates a bottom frame for the logout button."""
        bottom_frame = tk.Frame(self, bg="white", bd=1, relief="solid")
        bottom_frame.pack(side="bottom", fill="x", padx=10, pady=10)

        logout_button = tk.Button(bottom_frame, text="Logout", font=("Helvetica", 14), bg="red", fg="white",
                                  command=self.logout)
        logout_button.pack(side="left", padx=10, pady=5)

    def logout(self):
        """Handles logout and returns to the login page."""
        confirm = messagebox.askyesno("Logout", "Are you sure you want to logout?")
        if confirm:
            self.controller.show_frame("LoginPage")

    def add_store(self, store_name, store_location):
        """Add a new store to the database"""
        if not store_name or not store_location:
            messagebox.showerror("Error", "All fields must be filled out.")
            return

        try:
            query = "INSERT INTO stores (name, location) VALUES (%s, %s)"
            data = (store_name, store_location)
            sqlConnector.connect(query, data)

            messagebox.showinfo("Success", f"Store {store_name} added successfully!")
            self.populate_store_dropdowns()
        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    def update_store(self, current_store, new_name, new_location):
        """Update an existing store in the database"""
        if not current_store or not new_name or not new_location:
            messagebox.showerror("Error", "All fields must be filled out.")
            return

        try:
            query = "UPDATE stores SET name = %s, location = %s WHERE name = %s"
            data = (new_name, new_location, current_store)
            sqlConnector.connect(query, data)

            messagebox.showinfo("Success", f"Store {current_store} updated successfully!")
            self.populate_store_dropdowns()
        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    def delete_store(self, store_name):
        """Delete a store from the database"""
        if not store_name:
            messagebox.showerror("Error", "Please select a store to delete.")
            return

        confirm = messagebox.askyesno("Confirm", f"Are you sure you want to delete {store_name}?")
        if not confirm:
            return

        try:
            query = "DELETE FROM stores WHERE name = %s"
            data = (store_name,)
            sqlConnector.connect(query, data)

            messagebox.showinfo("Success", f"Store {store_name} deleted successfully!")
            self.populate_store_dropdowns()
        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    def populate_store_dropdowns(self):
        """Populate store dropdowns with stores from the database"""
        try:
            query = "SELECT name FROM stores"
            results = sqlConnector.connect(query, ())

            if not results or not isinstance(results, list):
                return

            store_names = [row[0] for row in results]

            # Find and update all OptionMenus
            for widget in self.winfo_children():
                for subwidget in widget.winfo_children():
                    if isinstance(subwidget, tk.OptionMenu):
                        menu = subwidget["menu"]
                        menu.delete(0, "end")
                        var = subwidget.cget("textvariable")
                        for store in store_names:
                            menu.add_command(label=store, command=tk._setit(var, store))
        except Exception as e:
            messagebox.showerror("Database Error", str(e))

# For testing purposes, run this file directly.
if __name__ == '__main__':
    root = tk.Tk()
    root.title("EMS Application - Owner Page")
    root.geometry("900x750")
    app = OwnerPage(root, None)
    app.pack(fill="both", expand=True)
    root.mainloop()