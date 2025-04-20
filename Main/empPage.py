import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from tkinter import ttk
import sqlConnector
from Tabs.closeOutTab import CloseOutTab

# Color definitions
BG_COLOR = "white"
FG_COLOR = "black"
TAB_BG_COLOR = "white"
BUTTON_FG_COLOR = "black"
LOGOUT_BG_COLOR = "red"
LOGOUT_FG_COLOR = "white"
TITLE_FONT = ("Helvetica", 14)
ENTRY_FONT = ("Helvetica", 14)
LABEL_FONT = ("Helvetica", 18)
BUTTON_FONT = ("Helvetica", 14)

class EmployeePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg=BG_COLOR)
        self.create_top_frame()
        self.create_bottom_frame()
        self.createMiddleFrame()

        # Access session info
        employee_id = self.controller.employee_id
        username = self.controller.username
        print(f"Welcome, {username} (ID: {employee_id})")
    # creates the top part
    def create_top_frame(self):
        # Top frame for store selection dropdown
        top_frame = tk.Frame(self, bg=BG_COLOR, bd=1, relief="solid")
        top_frame.pack(side="top", fill="x", padx=10, pady=10)

        # Centered label (ALOHA)
        aloha_label = tk.Label(top_frame, text=self.controller.role, font=TITLE_FONT, bg=BG_COLOR, fg=FG_COLOR)
        aloha_label.place(relx=0.5, rely=0.5, anchor="center")

        # Right label (name of employee)
        tk.Label(top_frame, text=self.controller.username, font=TITLE_FONT, bg=BG_COLOR, fg=FG_COLOR).pack(side="right",
                                                                                                          padx=(5, 10))
        # select stores
        self.selected_store = tk.StringVar()
        # Fetch the first store name from the database
        query = "SELECT all store_name FROM Store"
        result = sqlConnector.connect(query, ())

        if result and result[0][0]:
            # Check if a store name is returned
            store_options = [store[0] for store in result if store[0] is not None]
            self.selected_store.set(result[0][0])  # Set the first store name as the default
            store_dropdown = tk.OptionMenu(top_frame, self.selected_store, *store_options)
            store_dropdown.config(font=("Helvetica", 14), bg="white", fg="black", relief="solid", bd=2)
            store_dropdown.pack(side="left", padx=10, pady=5)

    def createMiddleFrame(self):
        # Left frame for tab buttons
        tab_frame = tk.Frame(self, bg=BG_COLOR, width=220, bd=1, relief="solid")
        tab_frame.pack(side="left", fill="y", padx=10, pady=10)

        # Right frame for content
        content_frame = tk.Frame(self, bg=BG_COLOR, bd=1, relief="solid")
        content_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        content_frame.grid_rowconfigure(0, weight=1)
        content_frame.grid_columnconfigure(0, weight=1)

        # Dictionary to hold the tabs and their corresponding frames
        self.tabs = {}
        # Store clock-in/out history
        self.records = []

        # Clock-in tab
        reg_in = tk.Frame(content_frame, bg=BG_COLOR)
        reg_in.grid(row=0, column=0, sticky="nsew")
        tk.Label(reg_in, text="Enter Reg-In Balance", font=LABEL_FONT, bg=BG_COLOR, fg=FG_COLOR).pack(pady=10)
        self.reg_in_balance = tk.Entry(reg_in, font=ENTRY_FONT)
        self.reg_in_balance.pack(pady=5)
        tk.Button(reg_in, text="Submit and Clock In", font=BUTTON_FONT, command=self.clock_in).pack(pady=10)
        self.tabs["Clock in"] = reg_in

        # Clock-out tab
        reg_out = tk.Frame(content_frame, bg=BG_COLOR)
        reg_out.grid(row=0, column=0, sticky="nsew")
        tk.Label(reg_out, text="Enter Reg-Out Balance", font=LABEL_FONT, bg=BG_COLOR, fg=FG_COLOR).pack(pady=10)
        self.reg_out_balance = tk.Entry(reg_out, font=ENTRY_FONT)
        self.reg_out_balance.pack(pady=5)
        tk.Button(reg_out, text="Submit and Clock Out", font=BUTTON_FONT, command=self.clock_out).pack(pady=10)
        self.tabs["Clock out"] = reg_out

        #close out tab
        close_out = CloseOutTab(content_frame, self.controller, self.selected_store)
        close_out.grid(row=0, column=0, sticky="nsew")
        self.tabs["Close Out"] = close_out

        # History tab
        history_tab = tk.Frame(content_frame, bg=BG_COLOR)
        tk.Label(history_tab, text="Clock In/Out History", font=LABEL_FONT, bg=BG_COLOR, fg=FG_COLOR).pack(pady=10)

        history_frame = tk.Frame(history_tab)
        history_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # define columns
        self.history_treeview = ttk.Treeview(
            history_frame,
            columns=( "last name ", "Store", "Clock In", "Reg In", "Clock Out", "Reg Out", "Reg gain","Duration"),
            show="headings"
        )

        # Define headings
        for col in ( "last name ","Store", "Clock In", "Reg In", "Clock Out", "Reg Out", "Reg gain","Duration"):
            self.history_treeview.heading(col, text=col)
            self.history_treeview.column(col, width=120, anchor="center")

        # Scrollbar for the treeview
        history_scrollbar = tk.Scrollbar(history_frame, orient="vertical", command=self.history_treeview.yview)
        self.history_treeview.configure(yscrollcommand=history_scrollbar.set)

        self.history_treeview.pack(side="left", fill="both", expand=True)
        history_scrollbar.pack(side="right", fill="y")

        self.tabs["History"] = history_tab

        # Function to switch tabs
        def show_tab(tab_name):
            for frame in self.tabs.values():
                frame.grid_forget()  # Hide all tabs
            self.tabs[tab_name].grid(row=0, column=0, sticky="nsew")  # Show the selected tab

            # Update the history tab content when it's shown
            if tab_name == "History":
                self.update_history()

        # Create tab buttons
        for title in self.tabs.keys():
            btn = tk.Button(tab_frame, text=title, font=BUTTON_FONT, fg=FG_COLOR, bg=TAB_BG_COLOR,
                            relief="solid", bd=2, command=lambda t=title: show_tab(t), width=25, height=2)
            btn.pack(pady=5, padx=10, fill="x")
        # shows clock in as the opening tab
        show_tab("Clock in")

    # bottom frame containing logout
    def create_bottom_frame(self):
        bottom_frame = tk.Frame(self, bg=BG_COLOR, bd=1, relief="solid")
        bottom_frame.pack(side="bottom", fill="x", padx=10, pady=10)

        logout_button = tk.Button(bottom_frame, text="Logout", font=BUTTON_FONT, bg=LOGOUT_BG_COLOR, fg=LOGOUT_FG_COLOR,
                                  command=self.logout)
        logout_button.pack(side="left", padx=10, pady=5)

    # confirms logout
    def logout(self):
        confirm = messagebox.askyesno("Logout", "Are you sure you want to logout?")
        if confirm:
            self.controller.show_frame("LoginPage")

    # clock in
    def clock_in(self):
        print("got in clock in")
        balance = self.reg_in_balance.get()
        if not balance:
            messagebox.showerror("Error", "Please enter a register balance.")
            return
        else:
            print("got a balance")


        store_name = self.selected_store.get()
        date= datetime.now().strftime("%Y-%m-%d")
        clock_in = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        reg_in = float(balance)
        clock_out = None
        reg_out = None
        employee_id = self.controller.employee_id

        # get first and last name
        queryFL = "SELECT firstName, lastName FROM employee WHERE employee_id = %s"
        result = sqlConnector.connect(queryFL, (employee_id,))
        print(result)
        firstName, lastName = result[0]
        print(firstName, lastName)

        # Check if the user has already clocked in today
        for record in self.records:
            if record["date"] == date and record["employee_id"] == employee_id and record["clock_in"] is not None:
                messagebox.showerror("Error", "You have already clocked in today.")
                return
            else:
                print("not clocked in yet")


        self.records.append({
            "last name": lastName,
            "store": store_name,
            "clock_in": clock_in,
            "reg_in": reg_in,
            "clock_out": clock_out,
            "reg_out": reg_out,
            "reg gain": "-",
            "duration": "-"
        })

        print(self.records)
        # sends info to databases
        query = """INSERT INTO clockTable (firstName,lastName,employee_id, clock_in, reg_in)
               VALUES (%s, %s,%s,%s,%s)"""
        data = (firstName,lastName,employee_id,clock_in, reg_in)

        try:
            # Send the data to the SQL connector
            sqlConnector.connect(query, data)
            messagebox.showinfo("Clock In", "Clock-in recorded successfully.")

        except Exception as e:
            messagebox.showerror("Database Error", f"An error occurred: {str(e)}")

        # Update the history display
        self.update_history()

    def clock_out(self):
        balance = self.reg_out_balance.get()
        if not balance:
            messagebox.showerror("Error", "Please enter a register balance.")
            return
        else:
            print("got a balance")



        reg_out = float(balance)
        employee_id = self.controller.employee_id
        clock_out_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


        # Fetch the most recent clock-in entry without a clock-out
        select_query = """SELECT clock_id, clock_in FROM clockTable
            WHERE employee_id = %s AND clock_out IS NULL
            ORDER BY clock_id DESC LIMIT 1
        """
        result = sqlConnector.connect(select_query, (employee_id,))
        print(result)
        if not result:
            messagebox.showerror("Error", "No matching clock-in found.")
            return
        clock_id, clock_in_str = result[0]

        # Update clockTable with clock-out info
        update_query = """
            UPDATE clockTable
            SET clock_out = %s, reg_out = %s
            WHERE clock_id = %s
        """
        sqlConnector.connect(update_query, (clock_out_time, reg_out, clock_id))


        # Get reg_in from the last record (local memory)
        last_record = self.records[-1]
        reg_gain = reg_out - last_record["reg_in"]

        print("before duration")

        # Get duration from the database using the clock_id
        query = "SELECT duration FROM clockTable WHERE clock_id = %s"
        data = (clock_id,)  # Use clock_id to fetch the correct record
        result = sqlConnector.connect(query, data)

        # Check if the result is valid
        if result:
            duration = result[0][0]  # Extract the duration value
        else:
            duration = None
            print("Duration not found for the given clock_id.")


        # Update local records
        self.records[-1].update({
            "clock_out": clock_out_time,
            "reg_out": reg_out,
            "reg gain": round(reg_gain, 2),
            "duration": duration
        })

        self.update_history()
        messagebox.showinfo("Clock Out", "Clock-out recorded successfully.")

    def update_history(self):
        self.history_treeview.delete(*self.history_treeview.get_children())
        for record in self.records:
            self.history_treeview.insert("", "end", values=tuple(record.values()))

