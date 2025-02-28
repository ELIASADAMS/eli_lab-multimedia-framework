import tkinter as tk
import tkinter.ttk as ttk
import subprocess
import os
import tkinter.messagebox
import signal  # Import the signal module
import sys


processes = []  # List to store references to child processes


def run_script(script_name):
    """Runs the specified Python script."""
    process = None  # Initialize process to None
    try:
        script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), script_name + ".py")
        process = subprocess.Popen(["python", script_path])  # Store the process object
        processes.append(process)  # Save this to kill after closing

    except FileNotFoundError:
        tk.messagebox.showerror("Error", f"{script_name}.py not found.")
    except Exception as e:
        tk.messagebox.showerror("Error", f"Error running {script_name}.py: {e}")
    finally:
        if not process:
            processes.remove(process)  # Remove process in case it's None


def on_closing():
    """Handles the window closing event."""
    for process in processes[:]:  # Iterate through a copy of the list to allow deletion
        if process is not None and process.poll() is None:  # If the process exists and is still running
            if sys.platform == 'win32':
                process.terminate()  # For Windows
            else:
                process.send_signal(signal.SIGTERM)  # Send a termination signal (SIGTERM)

            process.wait()  # Wait for the process to finish
        processes.remove(process)
    root.destroy()  # Close main window after killing subprocess


root = tk.Tk()
root.title("eli_lab Multimedia Framework")
root.geometry("450x700")  # Set initial window size

# Color scheme and styles (customizable)
style = ttk.Style()
style.theme_use('clam')

# Configure colors and fonts
font_name = "Bahnschrift"  # Define the font
style.configure('.', background='#2e2e2e', foreground='white', font=(font_name, 10))  # General background and text
style.configure('TFrame', background='#2e2e2e')  # Background for frames
style.configure('TLabel', background='#2e2e2e', foreground='white', padding=10, font=(font_name, 12, 'bold'))  # Headers
style.configure('TButton', background='#4a4a4a', foreground='white', padding=10, relief='flat', font=(font_name, 11),
                borderwidth=0, focuscolor='gray',
                activebackground='#606060',  # Color when pressed
                activeforeground='white')
style.map('TButton',
          background=[('active', '#606060'), ('disabled', '#4a4a4a')],
          foreground=[('disabled', 'gray')])

# Main container
main_frame = ttk.Frame(root, padding=20)
main_frame.pack(expand=True, fill='both')

# Title
title_label = ttk.Label(main_frame, text="eli_lab Multimedia Framework", font=(font_name, 20, 'bold'), anchor="center")
title_label.pack(pady=(0, 20))  # Add padding above and below

# Categories and scripts
categories = {
    "Project Structure Management": [
        ("Advanced Template System", "advanced_template_system"),
        ("Project Metadata Integration", "project_metadata_integration"),
        ("DCC Project Creation Hook", "dcc_project_creation_hook"),
    ],
    "Project Automation": [
        ("Texture Batch Optimising Tool", "texture_batch_optimising_tool"),
        ("Custom File Renaming", "custom_file_renaming"),
        ("Automated Project Clean", "automated_project_clean"),
    ],
    "Data Management": [
        ("File Validation", "file_validation"),
        ("Asset Reporting", "asset_reporting"),
        ("Project Validation", "project_validation"),
    ],
}

# Creating widgets
for category, scripts in categories.items():
    category_frame = ttk.Frame(main_frame, padding=(10, 0, 10, 10))
    category_frame.pack(fill='x', padx=10, pady=5)

    category_label = ttk.Label(category_frame, text=category, anchor='w')
    category_label.pack(fill='x')  # Occupy the entire width

    for func_name, script_name in scripts:
        button = ttk.Button(category_frame, text=func_name,
                            command=lambda script=script_name: run_script(script))
        button.pack(fill='x', pady=2)  # Stretch buttons to full width

root.protocol("WM_DELETE_WINDOW", on_closing)  # Intercept the close event

root.mainloop()
