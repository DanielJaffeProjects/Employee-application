import tkinter as tk
from tkinter import ttk
from Main.sqlConnector import connect
from Main.Notification import show_notification


class AddEmployee(tk.Frame):
    def __init__(self, parent,role):
        super().__init__(parent)
        self.configure(bg="white")

        # Title
        tk.Label(self, text="Manage Employees", font=("Helvetica", 18), bg="white").pack(pady=10)

        # First Name
        tk.Label(self, text="First Name:", font=("Helvetica", 14), bg="white").pack()
        self.first_name = tk.Entry(self, font=("Helvetica", 14))
        self.first_name.pack()

        # Last Name
        tk.Label(self, text="Last Name:", font=("Helvetica", 14), bg="white").pack()
        self.last_name = tk.Entry(self, font=("Helvetica", 14))
        self.last_name.pack()

        # Username
        tk.Label(self, text="Username:", font=("Helvetica", 14), bg="white").pack()
        self.username = tk.Entry(self, font=("Helvetica", 14))
        self.username.pack()

        # Password
        tk.Label(self, text="Password:", font=("Helvetica", 14), bg="white").pack()
        self.password = tk.Entry(self, font=("Helvetica", 14), show="*")
        self.password.pack()

        if role.lower() == "owner":
            # Role Dropdown
            tk.Label(self, text="Role:", font=("Helvetica", 14), bg="white").pack()
            self.role = ttk.Combobox(self, values=["employee", "manager", "owner"], font=("Helvetica", 14))
            self.role.pack()
        elif role.lower() == "manager":
            # Role Dropdown
            tk.Label(self, text="Role:", font=("Helvetica", 14), bg="white").pack()
            self.role = ttk.Combobox(self, values=["employee", "manager"], font=("Helvetica", 14))
            self.role.pack()

        # Add Employee Button
        tk.Button(self, text="Add Employee", font=("Helvetica", 14), bg="green", fg="white",
                  command=self.add_employee).pack(pady=10)

        # Delete Employee Section
        tk.Label(self, text="Delete Employee", font=("Helvetica", 16), bg="white").pack(pady=10)
        self.delete_username = ttk.Combobox(self, font=("Helvetica", 14))
        self.delete_username.pack()
        tk.Button(self, text="Delete Employee", font=("Helvetica", 14), bg="red", fg="white",
                  command=self.delete_employee).pack(pady=10)

        # Edit Employee Section
        tk.Label(self, text="Edit Employee", font=("Helvetica", 16), bg="white").pack(pady=10)
        self.edit_username = ttk.Combobox(self, font=("Helvetica", 14))
        self.edit_username.pack()
        tk.Button(self, text="Load Employee", font=("Helvetica", 14), bg="blue", fg="white",
                  command=self.load_employee).pack(pady=10)
        tk.Button(self, text="Update Employee", font=("Helvetica", 14), bg="orange", fg="white",
                  command=self.update_employee).pack(pady=10)

        # Load employee usernames for delete/edit
        self.load_usernames()

    def add_employee(self):
        """Handles adding a new employee to the database."""
        first_name = self.first_name.get()
        last_name = self.last_name.get()
        username = self.username.get()
        password = self.password.get()
        role = self.role.get()

        # Validate input
        if not all([first_name, last_name, username, password, role]):
            show_notification("All fields must be filled out.")
            return

        try:
            # Insert into the database
            query = """INSERT INTO employee (firstName, lastName, userName, password, role)
                       VALUES (%s, %s, %s, %s, %s)"""
            data = (first_name, last_name, username, password, role)
            success = connect(query, data)

            if success:
                show_notification("Employee added successfully!")
                self.clear_form()
                self.load_usernames()
            else:
                show_notification("Failed to add employee.")
        except Exception as e:
            show_notification( f"An error occurred: {e}")

    def delete_employee(self):
        """Handles deleting an employee from the database."""
        username = self.delete_username.get()
        if not username:
            show_notification("Please select an employee to delete.")
            return

        try:
            query = "DELETE FROM employee WHERE userName = %s"
            success = connect(query, (username,))
            if success:
                show_notification( f"Employee '{username}' deleted successfully!")
                self.load_usernames()
            else:
                show_notification("Failed to delete employee.")
        except Exception as e:
            show_notification( f"An error occurred: {e}")

    def load_employee(self):
        """Loads an employee's data into the form for editing."""
        username = self.edit_username.get()
        if not username:
            show_notification("Please select an employee to edit.")
            return

        try:
            query = "SELECT firstName, lastName, userName, password, role FROM employee WHERE userName = %s"
            result = connect(query, (username,))
            if result:
                first_name, last_name, username, password, role = result[0]
                self.first_name.delete(0, tk.END)
                self.first_name.insert(0, first_name)
                self.last_name.delete(0, tk.END)
                self.last_name.insert(0, last_name)
                self.username.delete(0, tk.END)
                self.username.insert(0, username)
                self.password.delete(0, tk.END)
                self.password.insert(0, password)
                self.role.set(role)
            else:
                show_notification("Failed to load employee data.")
        except Exception as e:
            show_notification(f"An error occurred: {e}")

    def update_employee(self):
        """Updates an employee's data in the database."""
        first_name = self.first_name.get()
        last_name = self.last_name.get()
        username = self.username.get()
        password = self.password.get()
        role = self.role.get()

        # Validate input
        if not all([first_name, last_name, username, password, role]):
            show_notification("All fields must be filled out.")
            return

        try:
            query = """UPDATE employee
                       SET firstName = %s, lastName = %s, password = %s, role = %s
                       WHERE userName = %s"""
            data = (first_name, last_name, password, role, username)
            success = connect(query, data)
            if success:
                show_notification("Employee updated successfully!")
                self.clear_form()
                self.load_usernames()
            else:
                show_notification("Failed to update employee.")
        except Exception as e:
            show_notification( f"An error occurred: {e}")

    def load_usernames(self):
        """Loads all employee usernames into the dropdowns."""
        try:
            query = "SELECT userName FROM employee"
            result = connect(query, ())
            usernames = [row[0] for row in result]
            self.delete_username['values'] = usernames
            self.edit_username['values'] = usernames
        except Exception as e:
            show_notification( f"An error occurred: {e}")

    def clear_form(self):
        """Clears the form fields."""
        self.first_name.delete(0, tk.END)
        self.last_name.delete(0, tk.END)
        self.username.delete(0, tk.END)
        self.password.delete(0, tk.END)
        self.role.set("")


