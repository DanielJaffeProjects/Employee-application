# 🧑‍💼✨ Employee Management System (EMS)

Welcome to the **Employee Management System** — a desktop application built with **Python**, **Tkinter**, and **MySQL**. This system is designed to streamline the management of employees, stores, payroll, clock-ins, and more, all within a user-friendly interface.

🎯 Built for **Owners**, **Managers**, and **Employees**, the EMS provides **role-based features** to cater to the specific needs of each user type.

---

## 🚀 Features at a Glance

| 👤 Role     | 🔧 Capabilities                                                                                           |
|------------|-----------------------------------------------------------------------------------------------------------|
| 🧑‍💼 **Employee** | ⏱ Clock In/Out, 🧾 Submit Daily Close, 🕓 View History                                                    |
| 🧑‍💼 **Manager** | 🧾 Submit Invoices, 💸 Track Expenses, 📦 Manage Merchandise, 📊 monthly reports on employees, 💵 Payroll |
| 🧑‍💼 **Owner**   | 🏪 Add/Edit/Delete Stores, Withdraws, 🔍 View All Store Data, everything that manager can do              |

---

## 🛠 Tech Stack

- 🐍 **Python 3**: Core programming language.
- 🪟 **Tkinter**: For building the graphical user interface (GUI).
- 🛢 **MySQL**: Database management using `mysql-connector-python`.
- 🧩 **Modular File System**: Organized codebase for scalability and maintainability.
- 📦 **Custom `sqlConnector.py`**: Handles all database operations.

---

## 📂 Project Structure

- **`Tabs/updateEmployees.py`**:  
  Handles employee management, including adding, editing, and deleting employee records. Features include:
  - Loading employee data into forms for editing.
  - Updating employee details in the database.
  - Validating input fields to ensure data integrity.
  - Managing dropdowns for employee usernames.

- **`Tabs/Store.py`**:  
  Manages store-related operations, such as:
  - Adding new stores with validation to prevent duplicates.
  - Deleting stores from the database.
  - Displaying store records in a Treeview widget.
  - Loading all stores dynamically from the database.

- **`sqlConnector.py`**:  
  A custom module for database connectivity and query execution.

---

## 🖥 How to Run

1. **Install Dependencies**:
   Ensure you have Python 3 and MySQL installed. Install the required Python packages using:
   ```bash
   pip install mysql-connector-python
   ...
   # Note make sure to be running the Main-branch
   # first run the database.sql file to create the database and tables
   # then run the ems file as that is the one that will run the main program
   # From there sit back and watch the magic happen
   