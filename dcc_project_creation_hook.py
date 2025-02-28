import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os


# Function to create a new Blender project
def create_project():
    project_name = project_name_entry.get()
    project_path = project_path_entry.get()
    render_path = render_path_entry.get()
    working_units = working_units_entry.get()
    library_path = library_path_entry.get()

    if project_name and project_path and render_path:
        full_path = os.path.join(project_path, project_name)
        try:
            os.makedirs(full_path)  # Create the directory for the project

            # Create subdirectories for the project
            os.makedirs(os.path.join(full_path, 'characters'))
            os.makedirs(os.path.join(full_path, 'assets'))
            os.makedirs(os.path.join(full_path, 'locations'))
            os.makedirs(os.path.join(full_path, 'renders'))

            # Create a basic Blender scene file
            scene_file_path = os.path.join(full_path, f"{project_name}.blend")

            # Create a basic scene file (this is a placeholder, you can modify it to read from your existing library)
            with open(scene_file_path, 'w') as f:
                f.write(f"# Blender project file for {project_name}\n")
                f.write(f"# Render Path: {render_path}\n")
                f.write(f"# Working Units: {working_units}\n")
                f.write(f"# Library Path: {library_path}\n")
                f.write("# Add your Blender scene setup here...\n")

            messagebox.showinfo("Success", f"Blender Project '{project_name}' created successfully at:\n{full_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create project: {e}")
    else:
        messagebox.showwarning("Input Error", "Please fill in all fields.")


# Function to browse for a project directory
def browse_directory():
    selected_directory = filedialog.askdirectory()
    if selected_directory:  # If a directory is selected
        project_path_entry.delete(0, tk.END)  # Clear the entry
        project_path_entry.insert(0, selected_directory)  # Insert the selected path


# Function to browse for a render directory
def browse_render_directory():
    selected_directory = filedialog.askdirectory()
    if selected_directory:  # If a directory is selected
        render_path_entry.delete(0, tk.END)  # Clear the entry
        render_path_entry.insert(0, selected_directory)  # Insert the selected path


# Function to browse for a library directory
def browse_library_directory():
    selected_directory = filedialog.askdirectory()
    if selected_directory:  # If a directory is selected
        library_path_entry.delete(0, tk.END)  # Clear the entry
        library_path_entry.insert(0, selected_directory)  # Insert the selected path


# Create the main application window
root = tk.Tk()
root.title("Blender Project Creation Hook")
root.geometry("600x600")

# Color scheme and styles (customizable)
style = ttk.Style()
style.theme_use('clam')

# Configure colors and fonts
font_name = "Bahnschrift"
style.configure('.', background='#2e2e2e', foreground='white', font=(font_name, 10))
style.configure('TFrame', background='#2e2e2e')
style.configure('TLabel', background='#2e2e2e', foreground='white', padding=10, font=(font_name, 12, 'bold'))
style.configure('TButton', background='#4a4a4a', foreground='white', padding=10, relief='flat', font=(font_name, 11),
                borderwidth=0, focuscolor='gray',
                activebackground='#606060',
                activeforeground='white')
style.map('TButton',
          background=[('active', '#606060'), ('disabled', '#4a4a4a')],
          foreground=[('disabled', 'gray')])

# Create a frame for the content
frame = ttk.Frame(root)
frame.pack(padx=0, pady=0, fill='both', expand=True)

# Project name label and entry
project_name_label = ttk.Label(frame, text="Project Name:")
project_name_label.pack(pady=(10, 10))

project_name_entry = ttk.Entry(frame, font=(font_name, 12))
project_name_entry.pack(pady=(0, 10))

# Project path label and entry
project_path_label = ttk.Label(frame, text="Project Path:")
project_path_label.pack(pady=(10, 10))

project_path_entry = ttk.Entry(frame, font=(font_name, 12))
project_path_entry.pack(pady=(0, 10))

# Browse button for project path
browse_button = ttk.Button(frame, text="Browse", command=browse_directory)
browse_button.pack(pady=(0, 10))

# Render path label and entry
render_path_label = ttk.Label(frame, text="Render Path:")
render_path_label.pack(pady=(10, 10))

render_path_entry = ttk.Entry(frame, font=(font_name, 12))
render_path_entry.pack(pady=(0, 10))

# Browse button for render path
browse_render_button = ttk.Button(frame, text="Browse for Render Path", command=browse_render_directory)
browse_render_button.pack(pady=(0, 10))

# Working units label and entry
working_units_label = ttk.Label(frame, text="Working Units:")
working_units_label.pack(pady=(10, 10))

working_units_entry = ttk.Entry(frame, font=(font_name, 12))
working_units_entry.pack(pady=(0, 10))

# Library path label and entry
library_path_label = ttk.Label(frame, text="Library Path:")
library_path_label.pack(pady=(10, 10))

library_path_entry = ttk.Entry(frame, font=(font_name, 12))
library_path_entry.pack(pady=(0, 10))

# Browse button for library path
browse_library_button = ttk.Button(frame, text="Browse for Library Path", command=browse_library_directory)
browse_library_button.pack(pady=(0, 10))

# Create project button
create_button = ttk.Button(frame, text="Create Project", command=create_project)
create_button.pack(pady=(20, 0))

# Start the main event loop
root.mainloop()
