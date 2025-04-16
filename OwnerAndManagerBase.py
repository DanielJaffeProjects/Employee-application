from tkinter import ttk
from datetime import datetime, timedelta

from Invoice import createInvoice
from Merchandise import create_merchandise_tab
from payroll import create_payroll_tab
from Store import *
from updateEmployees import AddEmployee

class ManageEmployees(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg="white")


        # Access session info
        employee_id = self.controller.employee_id
        username = self.controller.username

        # Initialize weekly start dates for Expenses, Merchandise, Gross Profit History (set to Monday)
        self.current_week_start = datetime.now().date() - timedelta(days=datetime.now().date().weekday())
        self.current_merch_week_start = datetime.now().date() - timedelta(days=datetime.now().date().weekday())
        self.current_profit_week_start = datetime.now().date() - timedelta(days=datetime.now().date().weekday())
        # For Employee History, initialize current date (daily)
        self.current_date = datetime.now().date()
        self.create_bottom_frame()
        # Top frame for store selection dropdown
        top_frame = tk.Frame(self, bg="white", bd=1, relief="solid")
        top_frame.pack(side="top", fill="x", padx=10, pady=10)

        # Centered label (ALOHA)
        aloha_label = tk.Label(top_frame, text=self.controller.role, font=("Helvetica", 14), bg="white", fg="black")
        aloha_label.place(relx=0.5, rely=0.5, anchor="center")




        # Right label (username of employee)
        tk.Label(top_frame, text=username, font=("Helvetica", 14), bg="white", fg="black").pack(side="right",
                                                                                                          padx=(5, 10))

        selected_store = tk.StringVar()
        # Fetch the first store name from the database
        query = "SELECT all store_name FROM Store"
        result = sqlConnector.connect(query, ())

        if result and result[0][0]:
            # Check if a store name is returned
            store_options = [store[0] for store in result if store[0] is not None]
            selected_store.set(result[0][0])  # Set the first store name as the default
            store_dropdown = tk.OptionMenu(top_frame, selected_store, *store_options)
            store_dropdown.config(font=("Helvetica", 14), bg="white", fg="black", relief="solid", bd=2)
            store_dropdown.pack(side="left", padx=10, pady=5)

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
        print(self.controller.role)
        if self.controller.role == 'Owner':
            print("In with draw")
            withdraw = tk.Frame(content_frame, bg="white")
            withdraw.grid(row=0, column=0, sticky="nsew")
            tabs["withdraw"] = withdraw

            tk.Label(withdraw, text="Gross Profit", font=("Helvetica", 18), bg="white").pack(pady=10)

            profit_nav_frame = tk.Frame(withdraw, bg="white")
            profit_nav_frame.pack(pady=10)
            prev_profit_btn = tk.Button(profit_nav_frame, text="<", font=("Helvetica", 14),
                                        command=self.previous_profit_week)
            prev_profit_btn.pack(side="left", padx=5)
            self.profit_week_label = tk.Label(profit_nav_frame, text="", font=("Helvetica", 14), bg="white")
            self.profit_week_label.pack(side="left", padx=5)
            next_profit_btn = tk.Button(profit_nav_frame, text=">", font=("Helvetica", 14),
                                        command=self.next_profit_week)
            next_profit_btn.pack(side="left", padx=5)

            tk.Label(withdraw, text="Enter Date (YYYY-MM-DD):", font=("Helvetica", 14), bg="white").pack(
                pady=(20, 5))
            self.profit_week_entry = tk.Entry(withdraw, font=("Helvetica", 14))
            self.profit_week_entry.pack(pady=5)
            tk.Button(withdraw, text="Go", font=("Helvetica", 14),
                      command=self.set_profit_week_from_entry).pack(pady=5)

            # Create a Treeview for the gross profit table
            self.gross_profit_tree = ttk.Treeview(withdraw, columns=("Date", "Cash", "Credit", "Total"),
                                                  show="headings")
            self.gross_profit_tree.heading("Date", text="Date")
            self.gross_profit_tree.heading("Cash", text="Cash")
            self.gross_profit_tree.heading("Credit", text="Credit")
            self.gross_profit_tree.heading("Total", text="Total")
            self.gross_profit_tree.pack(fill="both", expand=True, padx=10, pady=10)
            self.update_gross_profit_display()
        else:
            print("Not an owner, no withdraw tab added")



        # store tabs
        if self.controller.role == 'Owner':
            create_store_tab(content_frame, tabs, add_store, delete_store)

        if self.controller.role == 'Owner' or 'Manager':
            # make payroll
            create_payroll_tab(content_frame, tabs,employee_id)
            # add employee or update
            add_employee_tab = AddEmployee(content_frame)
            add_employee_tab.grid(row=0, column=0, sticky="nsew")
            tabs["Add Employee"] = add_employee_tab
            # submit a invoice
            createInvoice(content_frame, tabs)

            # merchandise
            create_merchandise_tab(content_frame, tabs)

        # -------------------------------
        # Enter Expense Tab
        # -------------------------------
        enter_expense_frame = tk.Frame(content_frame, bg="white")
        enter_expense_frame.grid(row=0, column=0, sticky="nsew")
        tk.Label(enter_expense_frame, text="Enter Expense", font=("Helvetica", 18), bg="white").pack(pady=10)

        tk.Label(enter_expense_frame, text="Expense Type:", font=("Helvetica", 14), bg="white").pack()
        expense_type = tk.Entry(enter_expense_frame, font=("Helvetica", 14))
        expense_type.pack()

        tk.Label(enter_expense_frame, text="Expense Value:", font=("Helvetica", 14), bg="white").pack()
        expense_value = tk.Entry(enter_expense_frame, font=("Helvetica", 14))
        expense_value.pack()

        tk.Label(enter_expense_frame, text="Expense Date:", font=("Helvetica", 14), bg="white").pack()
        expense_date = tk.Entry(enter_expense_frame, font=("Helvetica", 14))
        expense_date.pack()

        tk.Button(enter_expense_frame, text="Submit Expense", font=("Helvetica", 14),
                  command=lambda: self.submit_expense(expense_type.get(), expense_value.get(), expense_date.get())).pack(pady=10)

        tabs["Enter Expense"] = enter_expense_frame




        # -------------------------------
        # Gross Profit Tab (Weekly)
        # -------------------------------
        gross_profit_frame = tk.Frame(content_frame, bg="white")
        gross_profit_frame.grid(row=0, column=0, sticky="nsew")
        tabs["Gross Profit"] = gross_profit_frame

        tk.Label(gross_profit_frame, text="Gross Profit", font=("Helvetica", 18), bg="white").pack(pady=10)

        profit_nav_frame = tk.Frame(gross_profit_frame, bg="white")
        profit_nav_frame.pack(pady=10)
        prev_profit_btn = tk.Button(profit_nav_frame, text="<", font=("Helvetica", 14), command=self.previous_profit_week)
        prev_profit_btn.pack(side="left", padx=5)
        self.profit_week_label = tk.Label(profit_nav_frame, text="", font=("Helvetica", 14), bg="white")
        self.profit_week_label.pack(side="left", padx=5)
        next_profit_btn = tk.Button(profit_nav_frame, text=">", font=("Helvetica", 14), command=self.next_profit_week)
        next_profit_btn.pack(side="left", padx=5)

        tk.Label(gross_profit_frame, text="Enter Date (YYYY-MM-DD):", font=("Helvetica", 14), bg="white").pack(pady=(20,5))
        self.profit_week_entry = tk.Entry(gross_profit_frame, font=("Helvetica", 14))
        self.profit_week_entry.pack(pady=5)
        tk.Button(gross_profit_frame, text="Go", font=("Helvetica", 14), command=self.set_profit_week_from_entry).pack(pady=5)

        # Create a Treeview for the gross profit table
        self.gross_profit_tree = ttk.Treeview(gross_profit_frame, columns=("Date", "Cash", "Credit", "Total"), show="headings")
        self.gross_profit_tree.heading("Date", text="Date")
        self.gross_profit_tree.heading("Cash", text="Cash")
        self.gross_profit_tree.heading("Credit", text="Credit")
        self.gross_profit_tree.heading("Total", text="Total")
        self.gross_profit_tree.pack(fill="both", expand=True, padx=10, pady=10)
        self.update_gross_profit_display()

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
        show_tab("Enter Invoice")

    # -------------------------------
    # Placeholder Methods
    # -------------------------------

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


    def submit_expense(self, expense_type, expense_value, expense_date):
        messagebox.showinfo("Submit Expense", f"Expense '{expense_type}' submitted!")




    # -------------------------------
    # Gross Profit (Weekly) Methods
    # -------------------------------
    def update_gross_profit_display(self):
        profit_week_end = self.current_profit_week_start + timedelta(days=6)
        self.profit_week_label.config(text=f"{self.current_profit_week_start.strftime('%Y-%m-%d')} to {profit_week_end.strftime('%Y-%m-%d')}")
        # Clear the treeview
        for row in self.gross_profit_tree.get_children():
            self.gross_profit_tree.delete(row)
        # Insert a dummy row for each day of the week (placeholders)
        for i in range(7):
            day = self.current_profit_week_start + timedelta(days=i)
            self.gross_profit_tree.insert("", "end", values=(day.strftime("%Y-%m-%d"), "0", "0", "0"))

    def previous_profit_week(self):
        self.current_profit_week_start -= timedelta(weeks=1)
        self.update_gross_profit_display()

    def next_profit_week(self):
        self.current_profit_week_start += timedelta(weeks=1)
        self.update_gross_profit_display()

    def set_profit_week_from_entry(self):
        try:
            new_date = datetime.strptime(self.profit_week_entry.get(), "%Y-%m-%d").date()
            self.current_profit_week_start = new_date - timedelta(days=new_date.weekday())
            self.update_gross_profit_display()
        except ValueError:
            messagebox.showerror("Invalid Date", "Please enter a valid date in YYYY-MM-DD format.")
