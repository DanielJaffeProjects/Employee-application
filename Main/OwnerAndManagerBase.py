from datetime import datetime, timedelta

from Tabs.EmployeeData import create_employee_history_tab
from Tabs.Bonus import create_bonus_tab
from Tabs.Invoice import createInvoice
from Tabs.Merchandise import create_merchandise_tab
from Tabs.payroll import create_payroll_tab
from Tabs.Store import *
from Tabs.updateEmployees import AddEmployee
from Tabs.Expenses import create_expenses_tab
from Tabs.Withdraw import create_withdraw_tab
from Tabs.gross_profit import create_gross_profit_tab

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

        # for just the owner
        if self.controller.role == 'Owner':
            # make a store
            create_store_tab(content_frame, tabs, add_store, delete_store)

            # check employee history for 1 year
            create_employee_history_tab(content_frame, tabs,365)

            # withdraw
            create_withdraw_tab(content_frame, tabs)

        # if anyone sees this Daniel is the greatest of all time Easter egg!!
        # for owner and manager
        if self.controller.role == 'Owner' or 'Manager':
            # make payroll
            create_payroll_tab(content_frame, tabs,employee_id)

            # add employee or update
            add_employee_tab = AddEmployee(content_frame,self.controller.role)
            add_employee_tab.grid(row=0, column=0, sticky="nsew")
            tabs["Add Employee"] = add_employee_tab

            # submit a invoice
            createInvoice(content_frame, tabs)

            # merchandise
            create_merchandise_tab(content_frame, tabs)

            # Bonus
            create_bonus_tab(content_frame, tabs)

            # expenses
            create_expenses_tab(content_frame, tabs)

            # gross profit
            create_gross_profit_tab(content_frame, tabs)

        # for just the manager
        if self.controller.role == 'Manager':
            # check employee history for 30 days
            create_employee_history_tab(content_frame, tabs,30)

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

