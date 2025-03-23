import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from tkinter import ttk
import sqlConnector

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

    # creates the top part
    def create_top_frame(self):
        # Top frame for store selection dropdown
        top_frame = tk.Frame(self, bg=BG_COLOR, bd=1, relief="solid")
        top_frame.pack(side="top", fill="x", padx=10, pady=10)

        # Centered label (ALOHA)
        aloha_label = tk.Label(top_frame, text="ALOHA", font=TITLE_FONT, bg=BG_COLOR, fg=FG_COLOR)
        aloha_label.place(relx=0.5, rely=0.5, anchor="center")

        # Right label (name of employee)
        tk.Label(top_frame, text="Name of employee", font=TITLE_FONT, bg=BG_COLOR, fg=FG_COLOR).pack(side="right",
                                                                                                          padx=(5, 10))
        # select stores
        self.selected_store = tk.StringVar()
        self.selected_store.set("Store 1")
        store_options = ["Store 1", "Store 2", "Store 3", "Store 4"]
        store_dropdown = tk.OptionMenu(top_frame, self.selected_store, *store_options)
        store_dropdown.config(font=ENTRY_FONT, bg=BG_COLOR, fg=FG_COLOR, relief="solid", bd=2)
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

        # close out tab
        close_out = tk.Frame(content_frame, bg=BG_COLOR)
        close_out.grid(row=0, column=0, sticky="nsew")

        # Labels
        tk.Label(close_out, text="Enter credit", font=LABEL_FONT, bg=BG_COLOR, fg=FG_COLOR).pack(pady=10)
        self.credit_entry = tk.Entry(close_out, font=LABEL_FONT)
        self.credit_entry.pack(pady=10)

        tk.Label(close_out, text="Enter cash in envelope", font=LABEL_FONT, bg=BG_COLOR, fg=FG_COLOR).pack(pady=10)
        self.cash_entry = tk.Entry(close_out, font=LABEL_FONT)
        self.cash_entry.pack(pady=10)

        tk.Label(close_out, text="Enter expense", font=LABEL_FONT, bg=BG_COLOR, fg=FG_COLOR).pack(pady=10)
        self.expense_entry = tk.Entry(close_out, font=LABEL_FONT)
        self.expense_entry.pack(pady=10)

        tk.Label(close_out, text="Comments", font=LABEL_FONT, bg=BG_COLOR, fg=FG_COLOR).pack(pady=10)
        self.comments_entry = tk.Entry(close_out, font=LABEL_FONT)
        self.comments_entry.pack(pady=10)

        # submit button
        submit_button = tk.Button(close_out, text="Submit", font=LABEL_FONT, command=self.submit_info)
        submit_button.pack(pady=20)

        self.tabs["Close"] = close_out

        # History tab
        history_tab = tk.Frame(content_frame, bg=BG_COLOR)
        tk.Label(history_tab, text="Clock In/Out History", font=LABEL_FONT, bg=BG_COLOR, fg=FG_COLOR).pack(pady=10)

        history_frame = tk.Frame(history_tab)
        history_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # define columns
        self.history_treeview = ttk.Treeview(
            history_frame,
            columns=("Date", "Store", "Clock In", "Reg In", "Clock Out", "Reg Out", "Duration"),
            show="headings"
        )

        # Define headings
        for col in ("Date", "Store", "Clock In", "Reg In", "Clock Out", "Reg Out", "Duration"):
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
        balance = self.reg_in_balance.get()
        if not balance:
            messagebox.showerror("Error", "Please enter a register balance.")
            return
        date= datetime.now().strftime("%Y-%m-%d")
        store = self.selected_store.get()
        clock_in = datetime.now().strftime("%H:%M")
        reg_in = balance
        clock_out = None
        reg_out = None

        self.records.append({
            "date": date,
            "store": store,
            "clock_in": clock_in,
            "reg_in": reg_in,
            "clock_out": clock_out,
            "reg_out": reg_out,
            "duration": "-"
        })

        # sends info to database
        query = """INSERT INTO clockTable(reg_in)
           VALUES (%s)"""
        data = (reg_in,)

        # send data to sql connector
        sqlConnector.connect(query, data)
        messagebox.showinfo("Clock In", "Clock-in recorded successfully.")
        self.update_history()

    # clock out
    def clock_out(self):
        balance = self.reg_out_balance.get()
        if not balance:
            messagebox.showerror("Error", "Please enter a register balance.")
            return
        last_record = self.records[-1]
        last_record["clock_out"] = datetime.now().strftime("%H:%M")
        last_record["reg_out"] = balance

        in_time = datetime.strptime(last_record["clock_in"], "%H:%M")
        out_time = datetime.strptime(last_record["clock_out"], "%H:%M")
        last_record["duration"] = str(out_time - in_time)

        messagebox.showinfo("Clock Out", "Clock-out recorded successfully.")
        self.update_history()

    def update_history(self):
        self.history_treeview.delete(*self.history_treeview.get_children())
        for record in self.records:
            self.history_treeview.insert("", "end", values=tuple(record.values()))

    # Function to handle the submit button action
    def submit_info(self):
            credit = self.credit_entry.get()
            cash = self.cash_entry.get()
            expense = self.expense_entry.get()
            comments = self.comments_entry.get()
            storeName = self.selected_store.get()

            query = """INSERT INTO employee_close(firstName, lastName, store_name, credit, cash_in_envelope, expense, comments)
                VALUES (%s, %s, %s, %s, %s, %s,%s)"""
            data = (None, None,storeName, credit, cash, expense, comments)

            #send data to sql connector
            sqlConnector.connect(query, data)

if __name__ == '__main__':
    root = tk.Tk()
    root.title("Employee Dashboard")
    root.geometry("900x750")
    employee_page = EmployeePage(root, None)
    employee_page.pack(fill="both", expand=True)
    root.mainloop()
