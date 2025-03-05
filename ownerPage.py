import tkinter as tk
import login

class OwnerPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg="white")
        
        # Top frame for store selection dropdown
        top_frame = tk.Frame(self, bg="white", bd=1, relief="solid")
        top_frame.pack(side="top", fill="x", padx=10, pady=10)
        
        tk.Label(top_frame, text="Select Store:", font=("Helvetica", 14), bg="white", fg="black").pack(side="left", padx=(10,5))
        
        selected_store = tk.StringVar()
        selected_store.set("Store 1")  # default value
        store_options = ["Store 1", "Store 2", "Store 3", "Store 4"]
        store_dropdown = tk.OptionMenu(top_frame, selected_store, *store_options)
        store_dropdown.config(font=("Helvetica", 14), bg="white", fg="black", relief="solid", bd=2)
        store_dropdown.pack(side="left", padx=10, pady=5)
        
        # Main frame for tabs and content
        main_frame = tk.Frame(self, bg="white")
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Left frame for tabs
        tab_frame = tk.Frame(main_frame, bg="white", width=250, bd=1, relief="solid")
        tab_frame.pack(side="left", fill="y", padx=10, pady=10)
        
        # Right frame for content
        content_frame = tk.Frame(main_frame, bg="white", bd=1, relief="solid")
        content_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        content_frame.grid_rowconfigure(0, weight=1)
        content_frame.grid_columnconfigure(0, weight=1)
        
        # Tabs for Owner
        tabs = {}
        tab_titles = [
            "Enter Invoice", 
            "Enter Expense", 
            "Enter Merchandise Sales",
            "Enter Gross Profit", 
            "Withdrawal", 
            "Calculate Employee Bonus", 
            "Add Employee"
        ]
        
        for title in tab_titles:
            frame = tk.Frame(content_frame, bg="white")
            frame.grid(row=0, column=0, sticky="nsew")
            tk.Label(frame, text=title, font=("Helvetica", 18), bg="white", fg="black").pack(pady=40)
            tabs[title] = frame
            
        def show_tab(tab_name):
            tabs[tab_name].tkraise()
            
        for title in tab_titles:
            btn = tk.Button(
                tab_frame, text=title, font=("Helvetica", 14), fg="black", bg="white", relief="flat", bd=2,
                command=lambda t=title: show_tab(t), width=25, height=3
            )
            btn.pack(pady=5, padx=10, fill="x")
            
        # Logout button
        logout_button = tk.Button(
            tab_frame, 
            text="Logout", 
            font=("Helvetica", 14), 
            fg="black", 
            bg="white", 
            relief="flat", 
            bd=2, 
            command=lambda: controller.show_frame("LoginPage"),
            width=25, 
            height=3
        )
        logout_button.pack(side="bottom", pady=10, padx=10)
        
        # Show default tab
        show_tab(tab_titles[0])

if __name__ == '__main__':
    root = tk.Tk()
    root.title("Owner Dashboard")
    root.geometry("900x750")
    owner_page = OwnerPage(root, None)
    owner_page.pack(fill="both", expand=True)
    root.mainloop()
