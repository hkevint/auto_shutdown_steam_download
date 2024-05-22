import os
import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import ctypes
import time

# Path to the "downloading" folder in Steam apps
steam_downloading_path = "C:/Program Files (x86)/Steam/steamapps/downloading"

# Global state variables
queue_started = False
selected_action = None
countdown_seconds = 10
countdown_active = False

def update_status():
    """Update the status of the Steam download queue."""
    global queue_started
    # Check if the folder is empty
    if not os.listdir(steam_downloading_path):
        status_label.config(text="Queue Status: Finished", foreground="green")
        if queue_started and selected_action and not countdown_active:
            start_countdown()
    else:
        status_label.config(text="Queue Status: Downloading", foreground="red")
        queue_started = True
    
    # Schedule the function to run again after 1000 ms (1 second)
    root.after(1000, update_status)

def start_countdown():
    """Start the countdown for the selected action."""
    global countdown_active
    countdown_active = True
    show_cancel_dialog()
    countdown_label.grid(row=5, column=0, pady=10)
    countdown()

def countdown():
    """Perform the countdown and execute the selected action."""
    global countdown_seconds
    if countdown_seconds > 0:
        countdown_label.config(text=f"Action in {countdown_seconds} seconds...")
        countdown_seconds -= 1
        root.after(1000, countdown)
    else:
        execute_action()

def execute_action():
    """Execute the selected action (shutdown or sleep)."""
    root.quit()  # Close the program
    time.sleep(2)  # Wait 2 seconds
    if selected_action == "shutdown":
        subprocess.run(["shutdown", "/s", "/t", "0"])  # Shutdown the system
    elif selected_action == "sleep":
        ctypes.windll.powrprof.SetSuspendState(0, 1, 0)  # Sleep the system

def show_cancel_dialog():
    """Show a dialog to allow the user to cancel the action."""
    cancel_dialog = tk.Toplevel(root)
    cancel_dialog.title("Cancel Shutdown/Sleep")
    cancel_dialog.geometry("300x100")
    cancel_dialog.resizable(True, True)
    cancel_dialog.columnconfigure(0, weight=1)
    cancel_dialog.rowconfigure(0, weight=1)
    cancel_dialog.rowconfigure(1, weight=1)
    
    cancel_label = ttk.Label(cancel_dialog, text="The system will perform the selected action soon. Click 'Cancel' to abort.")
    cancel_label.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')
    
    cancel_button = ttk.Button(cancel_dialog, text="Cancel", command=lambda: cancel_action(cancel_dialog))
    cancel_button.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')

def cancel_action(dialog):
    """Cancel the action and close the dialog."""
    dialog.destroy()
    root.quit()

def toggle_shutdown():
    """Toggle the shutdown action."""
    global selected_action
    if shutdown_button.instate(['selected']):
        sleep_button.state(['!selected'])
        selected_action = "shutdown"
        action_label.config(text="Selected Action: Shutdown")
    else:
        selected_action = None
        action_label.config(text="Selected Action: None")

def toggle_sleep():
    """Toggle the sleep action."""
    global selected_action
    if sleep_button.instate(['selected']):
        shutdown_button.state(['!selected'])
        selected_action = "sleep"
        action_label.config(text="Selected Action: Sleep")
    else:
        selected_action = None
        action_label.config(text="Selected Action: None")

# Set up the main application window
root = tk.Tk()
root.title("Auto-Shutdown Steam Download")
root.geometry("450x450")
root.resizable(True, True)

# Configure the grid to expand with window size
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

# Create a frame for better layout management
frame = ttk.Frame(root, padding="20")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
frame.columnconfigure(0, weight=1)
frame.rowconfigure([0, 1, 2, 3, 4, 5], weight=1)

# Create a label for the live status
status_label = ttk.Label(frame, text="Queue Status: Checking...", font=('Helvetica', 12, 'bold'))
status_label.grid(row=0, column=0, pady=10, padx=10, sticky='nsew')

# Create toggle buttons for Shutdown and Sleep
shutdown_button = ttk.Checkbutton(frame, text="Shutdown", command=toggle_shutdown, style='TButton')
shutdown_button.grid(row=1, column=0, pady=10, padx=10, sticky='nsew')

sleep_button = ttk.Checkbutton(frame, text="Sleep", command=toggle_sleep, style='TButton')
sleep_button.grid(row=2, column=0, pady=10, padx=10, sticky='nsew')

# Create a label to show the selected action
action_label = ttk.Label(frame, text="Selected Action: None", font=('Helvetica', 12))
action_label.grid(row=3, column=0, pady=10, padx=10, sticky='nsew')

# Create a label to show the countdown
countdown_label = ttk.Label(frame, text="", font=('Helvetica', 12))

# Create a LabelFrame for the instructions
instructions_frame = ttk.LabelFrame(frame, text="Steps", padding="10")
instructions_frame.grid(row=4, column=0, pady=10, padx=10, sticky=(tk.W, tk.E, tk.N))
instructions_frame.columnconfigure(0, weight=1)

# Add instruction steps
steps = [
    "1. Select operation upon finished queue download (Shutdown or Sleep)",
    "2. Start Download Queue On Steam (drag Downloads/Updates in queue)",
    "3. Preferable to close/save anything on your computer.",
    "4. Let computer idle, it will execute desired execution upon finished queue.",
    "NOTE: A delay of 10 seconds will happen before shutdown/sleep, you can cancel operation before that."
]
for step in steps:
    step_label = ttk.Label(instructions_frame, text=step, font=('Helvetica', 10))
    step_label.grid(sticky=tk.W, pady=2)

# Run the status update function for the first time
update_status()

# Run the GUI loop
root.mainloop()
