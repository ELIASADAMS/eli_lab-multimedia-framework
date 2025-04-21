import os
import shutil
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

# --- Constants ---
BLENDER_FILES_DIR = r"D:\Ierarchy\ELI_LAB STUDIO\8. Coding\eli_lab-multimedia-framework\blender_files"  # Raw string for Windows path
TEMPLATE_FILES = {
    "eli_lab territory_assets": "Asset.blend",
    "eli_lab territory_characters": "Character.blend",
    "eli_lab territory_locations": "Location.blend",
}
OUTPUT_FILE_EXTENSION = ".blend"
TOP_LEVEL_FOLDERS = list(TEMPLATE_FILES.keys())  # list of top level directories


# --- Helper Functions ---
def create_blender_file(directory, template_path):
    """Copies a Blender template file to the specified directory, renaming it.

    Args:
        directory: The directory to copy the Blender file into.
        template_path: The path to the template Blender file.
    """
    folder_name = os.path.basename(directory).lower().replace(" ", "_")  # Get only the leaf folder name
    output_filename = folder_name + OUTPUT_FILE_EXTENSION
    output_path = os.path.join(directory, output_filename)

    try:
        shutil.copy2(template_path, output_path)  # Use copy2 to preserve metadata
        print(f"Created Blender file '{output_filename}' in '{directory}'")
    except Exception as e:
        print(f"Error creating Blender file in '{directory}': {e}")


def validate_project(root_directory, progress_callback=None, start_progress_callback=None, end_progress_callback=None):
    """Analyzes the directory structure and creates Blender files in leaf folders.

    Args:
        root_directory: The starting directory to analyze.
        progress_callback: A function to update the progress bar.
        start_progress_callback: function to initialize the progress bar
        end_progress_callback: function to finish the progress bar
    """

    leaf_folders = []
    # Traverse the directory tree and find leaf folders
    for root, dirs, files in os.walk(root_directory):
        if not dirs:
            leaf_folders.append(root)  # It's a leaf folder

    total_folders = len(leaf_folders)
    processed_folders = 0

    if start_progress_callback:
        start_progress_callback(total_folders)

    for leaf_folder in leaf_folders:
        # Get the list of parent directories
        parents = [os.path.basename(path) for path in leaf_folder.split(os.sep)[:-1]]

        # Find the top level parent that matches the keys in the template files
        top_level_parent = next((parent for parent in parents if parent in TOP_LEVEL_FOLDERS), None)

        # Check if parent is in Template files
        if top_level_parent in TEMPLATE_FILES:
            template_filename = TEMPLATE_FILES[top_level_parent]
            template_path = os.path.join(BLENDER_FILES_DIR, template_filename)
            if not os.path.isfile(template_path):
                print(f"Error: Template Blender file '{template_path}' not found.")
                continue
            create_blender_file(leaf_folder, template_path)
        else:
            print(f"Skipping '{leaf_folder}': No matching top-level parent directory in template list.")

        processed_folders += 1
        if progress_callback:
            progress_callback(processed_folders)

    if end_progress_callback:
        end_progress_callback()


# --- GUI Setup ---
root = tk.Tk()
root.title("Project Validation Tool")
root.geometry("600x350")

# --- Styling ---
style = ttk.Style(root)
style.theme_use('clam')

# Color scheme (from your previous code)
bg_color = '#2e2e2e'
fg_color = 'white'
text_color = '#d3d3d3'
button_bg_color = '#4a4a4a'
entry_bg_color = "#4a4a4a"
button_active_bg_color = '#606060'

style.configure('.', background=bg_color, foreground=fg_color, font=("Bahnschrift", 10))
style.configure('TLabel', background=bg_color, foreground=fg_color, padding=5, font=("Bahnschrift", 12))
style.configure('TButton', background=button_bg_color, foreground=fg_color, padding=8, relief='flat',
                font=("Bahnschrift", 11), borderwidth=0, focuscolor='gray',
                activebackground=button_active_bg_color, activeforeground=fg_color)
style.map('TButton',
          background=[('active', button_active_bg_color), ('disabled', button_bg_color)],
          foreground=[('disabled', 'gray')])
style.configure('TEntry', fieldbackground=entry_bg_color, foreground=text_color, font=("Bahnschrift", 11))
style.configure('Horizontal.TProgressbar', troughcolor=button_bg_color, background=fg_color)

# --- Main Frame ---
main_frame = ttk.Frame(root, padding=20)
main_frame.pack(expand=True, fill='both')

# --- Folder Selection ---
folder_label = ttk.Label(main_frame, text="Project Folder:")
folder_label.pack(pady=(0, 5), fill='x')

folder_path_entry = ttk.Entry(main_frame, width=50)
folder_path_entry.pack(pady=(0, 5), fill='x')


def browse_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        folder_path_entry.delete(0, tk.END)
        folder_path_entry.insert(0, folder_path)


browse_button = ttk.Button(main_frame, text="Browse", command=browse_folder)
browse_button.pack(pady=(0, 10), fill='x')

# --- Progress Bar ---
progress_bar = ttk.Progressbar(main_frame, orient="horizontal", length=400, mode="determinate")
progress_bar.pack(pady=(10, 15), fill='x')


# --- Validation Button ---
def start_validation():
    project_directory = folder_path_entry.get()
    if not project_directory:
        messagebox.showerror("Error", "Please select a project folder.")
        return

    # Disable GUI Elements
    validate_button["state"] = "disabled"
    browse_button["state"] = "disabled"

    def update_progress(value):
        progress_bar["value"] = value
        root.update_idletasks()

    def start_progress(max_value):
        progress_bar["maximum"] = max_value
        progress_bar["value"] = 0

    def end_progress():
        progress_bar["value"] = 0
        messagebox.showinfo("Info", "Project validation complete!")
        validate_button["state"] = "normal"  # Re-enable button
        browse_button["state"] = "normal"

    # Run validation in a separate thread
    threading.Thread(target=lambda: validate_project(
        project_directory,
        progress_callback=update_progress,
        start_progress_callback=start_progress,
        end_progress_callback=end_progress
    ), daemon=True).start()


validate_button = ttk.Button(main_frame, text="Validate Project", command=start_validation)
validate_button.pack(pady=(15, 0), fill='x')

# --- Run the GUI ---
root.mainloop()
