import tkinter as tk
from tkinter import messagebox
from datetime import datetime

class EmployeePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg="white")
        self.create_top_frame()
        self.create_bottom_frame()
        self.createRLframe()

    # creates the top part
    def create_top_frame(self):
        # Top frame for store selection dropdown
        top_frame = tk.Frame(self, bg="white", bd=1, relief="solid")
        top_frame.pack(side="top", fill="x", padx=10, pady=10)

        # Centered label (ALOHA)
        aloha_label = tk.Label(top_frame, text="ALOHA", font=("Helvetica", 14), bg="white", fg="black")
        aloha_label.place(relx=0.5, rely=0.5, anchor="center")

        # Right label (name of employee)
        tk.Label(top_frame, text="Name of employee", font=("Helvetica", 14), bg="white", fg="black").pack(side="right",
                                                                                                          padx=(5, 10))

        selected_store = tk.StringVar()
        selected_store.set("Store 1")
        store_options = ["Store 1", "Store 2", "Store 3", "Store 4"]
        store_dropdown = tk.OptionMenu(top_frame, selected_store, *store_options)
        store_dropdown.config(font=("Helvetica", 14), bg="white", fg="black", relief="solid", bd=2)
        store_dropdown.pack(side="left", padx=10, pady=5)
    def createRLframe(self):
        # Left frame for tab buttons
        tab_frame = tk.Frame(self, bg="white", width=220, bd=1, relief="solid")
        tab_frame.pack(side="left", fill="y", padx=10, pady=10)

        # Right frame for content
        content_frame = tk.Frame(self, bg="white", bd=1, relief="solid")
        content_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        content_frame.grid_rowconfigure(0, weight=1)
        content_frame.grid_columnconfigure(0, weight=1)

        # Dictionary to hold the tabs and their corresponding frames
        self.tabs = {}
        # Store clock-in/out history
        self.records = []

        # Clock-in tab
        reg_in = tk.Frame(content_frame, bg="white")
        reg_in.grid(row=0, column=0, sticky="nsew")
        tk.Label(reg_in, text="Enter Reg-In Balance", font=("Helvetica", 18), bg="white", fg="black").pack(pady=10)
        self.reg_in_balance = tk.Entry(reg_in, font=("Helvetica", 14))
        self.reg_in_balance.pack(pady=5)
        tk.Button(reg_in, text="Submit and Clock In", font=("Helvetica", 14), command=self.clock_in).pack(pady=10)
        self.tabs["Clock in"] = reg_in

        # Clock-out tab
        reg_out = tk.Frame(content_frame, bg="white")
        reg_out.grid(row=0, column=0, sticky="nsew")
        tk.Label(reg_out, text="Enter Reg-Out Balance", font=("Helvetica", 18), bg="white", fg="black").pack(pady=10)
        self.reg_out_balance = tk.Entry(reg_out, font=("Helvetica", 14))
        self.reg_out_balance.pack(pady=5)
        tk.Button(reg_out, text="Submit and Clock Out", font=("Helvetica", 14), command=self.clock_out).pack(pady=10)
        self.tabs["Clock out"] = reg_out

        # close out tab
        close_out = tk.Frame(content_frame, bg="white")
        close_out.grid(row=0, column=0, sticky="nsew")

        # Labels
        tk.Label(close_out, text="Enter credit", font=("Helvetica", 18), bg="white", fg="black").pack(pady=10)
        self.credit_entry = tk.Entry(close_out, font=("Helvetica", 18))
        self.credit_entry.pack(pady=10)

        tk.Label(close_out, text="Enter cash in envelope", font=("Helvetica", 18), bg="white", fg="black").pack(pady=10)
        self.cash_entry = tk.Entry(close_out, font=("Helvetica", 18))
        self.cash_entry.pack(pady=10)

        tk.Label(close_out, text="Enter expense", font=("Helvetica", 18), bg="white", fg="black").pack(pady=10)
        self.expense_entry = tk.Entry(close_out, font=("Helvetica", 18))
        self.expense_entry.pack(pady=10)

        tk.Label(close_out, text="Comments", font=("Helvetica", 18), bg="white", fg="black").pack(pady=10)
        self.comments_entry = tk.Entry(close_out, font=("Helvetica", 18))
        self.comments_entry.pack(pady=10)

        # submit button
        submit_button = tk.Button(close_out, text="Submit", font=("Helvetica", 18), command=self.submit_info)
        submit_button.pack(pady=20)

        self.tabs["Close"] = close_out

        # History tab
        history_tab = tk.Frame(content_frame, bg="white")
        tk.Label(history_tab, text="Clock In/Out History", font=("Helvetica", 18), bg="white", fg="black").pack(pady=10)

        history_frame = tk.Frame(history_tab)
        history_frame.pack(fill="both", expand=True, padx=10, pady=10)

        history_canvas = tk.Canvas(history_frame)
        history_scrollbar = tk.Scrollbar(history_frame, orient="vertical", command=history_canvas.yview)
        self.history_list_frame = tk.Frame(history_canvas)

        self.history_list_frame.bind("<Configure>", lambda e: history_canvas.configure(scrollregion=history_canvas.bbox("all")))
        history_canvas.create_window((0, 0), window=self.history_list_frame, anchor="nw")
        history_canvas.configure(yscrollcommand=history_scrollbar.set)

        history_canvas.pack(side="left", fill="both", expand=True)
        history_scrollbar.pack(side="right", fill="y")

        self.tabs["History"] = history_tab


        # Function to switch tabs
        def show_tab(tab_name):
            for frame in self.tabs.values():
                frame.grid_forget()  # Hide all tabs
            self.tabs[tab_name].grid(row=0, column=0, sticky="nsew")  # Show the selected tab

            if tab_name == "History":
                self.update_history()  # Update the history tab content when it's shown

        # Create tab buttons
        for title in self.tabs.keys():
            btn = tk.Button(tab_frame, text=title, font=("Helvetica", 14), fg="black", bg="white",
                            relief="solid", bd=2, command=lambda t=title: show_tab(t), width=25, height=2)
            btn.pack(pady=5, padx=10, fill="x")
        # shows clock in as the opening tab
        show_tab("Clock in")
    # bottom frame containing logout
    def create_bottom_frame(self):

        bottom_frame = tk.Frame(self, bg="white", bd=1, relief="solid")
        bottom_frame.pack(side="bottom", fill="x", padx=10, pady=10)

        logout_button = tk.Button(bottom_frame, text="Logout", font=("Helvetica", 14), bg="red", fg="white",
                                  command=self.logout)
        logout_button.pack(side="left", padx=10, pady=5)
    # confirms logout
    def logout(self):
        confirm = messagebox.askyesno("Logout", "Are you sure you want to logout?")
        if confirm:
            self.controller.show_frame("LoginPage")

    #clock in
    def clock_in(self):
        balance = self.reg_in_balance.get()
        if not balance:
            messagebox.showerror("Error", "Please enter a register balance.")
            return
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.records.append(f"Clock In: {timestamp} - Balance: {balance}")
        self.reg_in_balance.delete(0, tk.END)
        messagebox.showinfo("Clock In", "Clock-in recorded successfully.")
        self.update_history()
    # clock out
    def clock_out(self):
        balance = self.reg_out_balance.get()
        if not balance:
            messagebox.showerror("Error", "Please enter a register balance.")
            return
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.records.append(f"Clock Out: {timestamp} - Balance: {balance}")
        self.reg_out_balance.delete(0, tk.END)
        messagebox.showinfo("Clock Out", "Clock-out recorded successfully.")
        self.update_history()

    # updates the history for clock in and clock out
    def update_history(self):
        # Clear previous records in history
        for widget in self.history_list_frame.winfo_children():
            widget.destroy()

        # Display current records
        for record in self.records:
            tk.Label(self.history_list_frame, text=record, font=("Helvetica", 12), bg="white").pack(anchor="w", pady=2)

    # Function to handle the submit button action
    def submit_info(self):
        credit = self.credit_entry.get()
        cash = self.cash_entry.get()
        expense = self.expense_entry.get()
        comments = self.comments_entry.get()
if __name__ == '__main__':
    root = tk.Tk()
    root.title("Employee Dashboard")
    root.geometry("900x750")
    employee_page = EmployeePage(root, None)
    employee_page.pack(fill="both", expand=True)
    root.mainloop()
