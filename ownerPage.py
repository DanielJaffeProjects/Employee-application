import tkinter as tk
from tkinter import messagebox
import login

# used chatgpt to convert into subroutines to reduce repetition
class OwnerPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg="white")
        self.tabs = {}

        self.create_top_frame()
        self.create_main_frame()
        self.create_tabs()
        self.create_tab_buttons()
        self.create_bottom_frame()

    def create_top_frame(self):
        top_frame = tk.Frame(self, bg="white", bd=1, relief="solid")
        top_frame.pack(side="top", fill="x", padx=10, pady=10)

        aloha_label = tk.Label(top_frame, text="ALOHA", font=("Helvetica", 14), bg="white", fg="black")
        aloha_label.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(top_frame, text="Name of owner", font=("Helvetica", 14), bg="white", fg="black").pack(
            side="right", padx=(5, 10))

        selected_store = tk.StringVar()
        selected_store.set("Store 1")
        store_options = ["Store 1", "Store 2", "Store 3", "Store 4"]
        store_dropdown = tk.OptionMenu(top_frame, selected_store, *store_options)
        store_dropdown.config(font=("Helvetica", 14), bg="white", fg="black", relief="solid", bd=2)
        store_dropdown.pack(side="left", padx=10, pady=5)

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

    def create_main_frame(self):
        self.main_frame = tk.Frame(self, bg="white")
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.tab_frame = tk.Frame(self.main_frame, bg="white", width=250, bd=1, relief="solid")
        self.tab_frame.pack(side="left", fill="y", padx=10, pady=10)

        self.content_frame = tk.Frame(self.main_frame, bg="white", bd=1, relief="solid")
        self.content_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        self.content_frame.grid_rowconfigure(0, weight=1)
        self.content_frame.grid_columnconfigure(0, weight=1)

    def create_tabs(self):
        self.add_tab("Enter Invoice", ["Invoice ID", "Date", "Amount"], "Submit Invoice")
        self.add_tab("Enter Expense", ["Expense ID", "Date", "Amount", "Category"], "Submit Expense")
        self.add_tab("Enter Merchandise Sales", ["Sale ID", "Date", "Item", "Quantity", "Price"], "Submit Sale")
        self.add_tab("Enter Gross Profit", ["Total Revenue", "Total Expenses"], "Calculate Gross Profit")
        self.add_tab("Withdrawal", ["Withdrawal ID", "Date", "Amount"], "Submit Withdrawal")
        self.add_bonus_tab()
        self.add_employee_tab()

    def add_tab(self, name, fields, button_text):
        frame = tk.Frame(self.content_frame, bg="white")
        frame.grid(row=0, column=0, sticky="nsew")

        tk.Label(frame, text=name, font=("Helvetica", 18), bg="white", fg="black").pack(pady=10)
        entries = {}
        for field in fields:
            tk.Label(frame, text=f"{field}:", font=("Helvetica", 14), bg="white", fg="black").pack(pady=5)
            entries[field] = tk.Entry(frame, font=("Helvetica", 14))
            entries[field].pack(pady=5)

        tk.Button(frame, text=button_text, font=("Helvetica", 14),
                  command=lambda: messagebox.showinfo(name, f"{name} Submitted")).pack(pady=10)
        self.tabs[name] = frame

    def add_bonus_tab(self):
        frame = tk.Frame(self.content_frame, bg="white")
        frame.grid(row=0, column=0, sticky="nsew")

        tk.Label(frame, text="Calculate Employee Bonus", font=("Helvetica", 18), bg="white", fg="black").pack(
            pady=10)

        tk.Label(frame, text="Employee ID:", font=("Helvetica", 14), bg="white", fg="black").pack(pady=5)
        emp_id = tk.Entry(frame, font=("Helvetica", 14))
        emp_id.pack(pady=5)

        tk.Label(frame, text="Sales Amount:", font=("Helvetica", 14), bg="white", fg="black").pack(pady=5)
        sales_amt = tk.Entry(frame, font=("Helvetica", 14))
        sales_amt.pack(pady=5)

        tk.Label(frame, text="Bonus Percentage:", font=("Helvetica", 14), bg="white", fg="black").pack(pady=5)
        bonus_pct = tk.Entry(frame, font=("Helvetica", 14))
        bonus_pct.pack(pady=5)

        def calculate_bonus():
            try:
                sales = float(sales_amt.get())
                percent = float(bonus_pct.get())
                bonus = sales * percent / 100
                messagebox.showinfo("Bonus", f"Calculated Bonus: {bonus:.2f}")
            except ValueError:
                messagebox.showerror("Error", "Please enter valid numbers")

        tk.Button(frame, text="Calculate Bonus", font=("Helvetica", 14), command=calculate_bonus).pack(pady=10)
        self.tabs["Calculate Employee Bonus"] = frame

    def add_employee_tab(self):
        frame = tk.Frame(self.content_frame, bg="white")
        frame.grid(row=0, column=0, sticky="nsew")

        tk.Label(frame, text="Add Employee", font=("Helvetica", 18), bg="white", fg="black").pack(pady=10)

        tk.Label(frame, text="Employee Name:", font=("Helvetica", 14), bg="white", fg="black").pack(pady=5)
        emp_name = tk.Entry(frame, font=("Helvetica", 14))
        emp_name.pack(pady=5)

        tk.Label(frame, text="Role:", font=("Helvetica", 14), bg="white", fg="black").pack(pady=5)
        role_var = tk.StringVar(frame)
        role_var.set("employee")
        role_menu = tk.OptionMenu(frame, role_var, "employee", "manager", "owner")
        role_menu.config(font=("Helvetica", 14), bg="white", fg="black")
        role_menu.pack(pady=5)

        tk.Button(frame, text="Add Employee", font=("Helvetica", 14),
                  command=lambda: messagebox.showinfo("Add Employee", "Employee Added")).pack(pady=10)
        self.tabs["Add Employee"] = frame

    def create_tab_buttons(self):
        for title in self.tabs:
            tk.Button(self.tab_frame, text=title, font=("Helvetica", 14),
                      command=lambda t=title: self.show_tab(t), width=25, height=3).pack(pady=5, padx=10,
                                                                                         fill="x")

    def show_tab(self, tab_name):
        self.tabs[tab_name].tkraise()
