import tkinter as tk

def show_notification(message):
    """Displays a styled temporary notification in the bottom-right corner."""
    notification = tk.Toplevel()
    notification.overrideredirect(True)  # Remove window decorations
    notification.configure(bg="lightyellow", highlightbackground="black", highlightthickness=2)
    notification.attributes("-topmost", True)  # Keep the notification on top

    # Calculate dynamic width and height based on message length
    base_width = 300
    base_height = 70
    extra_width = min(len(message) * 7, 500)  # Limit max width to 500
    width = base_width + extra_width
    height = base_height + (len(message) // 50) * 20  # Adjust height for long messages

    # Set the size and position of the notification
    screen_width = notification.winfo_screenwidth()
    screen_height = notification.winfo_screenheight()
    x = screen_width - width - 10
    y = screen_height - height - 10
    notification.geometry(f"{width}x{height}+{x}+{y}")

    # Add the message to the notification
    label = tk.Label(
        notification,
        text=message,
        font=("Helvetica", 14, "bold"),
        bg="lightyellow",
        fg="black",
        wraplength=280,
        justify="center"
    )
    label.pack(expand=True, fill="both", padx=10, pady=10)

    # Fade-in effect
    for i in range(0, 11):
        notification.attributes("-alpha", i / 10)
        notification.update()
        notification.after(50)

    # Destroy the notification after 5 seconds
    notification.after(5000, notification.destroy)