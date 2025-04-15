import os
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from PIL import Image

# --- Constants ---
ALLOWED_EXTENSIONS = (".jpg", ".jpeg", ".tga", ".exr", ".hdr", ".bmp", ".gif", ".tiff", ".tif", ".png")


# --- Helper Functions ---
def is_image_file(filename):
    """Checks if a file has an image extension (case-insensitive)."""
    return filename.lower().endswith(ALLOWED_EXTENSIONS)


def convert_texture_to_png(filepath, output_dir, lock):
    try:
        if not os.path.isfile(filepath):
            print(f"Skipping '{filepath}' - not a valid file.")
            return False

        filename = os.path.basename(filepath)
        if not is_image_file(filename):
            print(f"Skipping '{filename}' - not an image file.")
            return False

        # Skip if already a PNG
        if filename.lower().endswith(".png"):
            print(f"Skipping '{filename}' - already a PNG")
            return False

        img = Image.open(filepath)
        name, _ = os.path.splitext(filename)
        output_path = os.path.join(output_dir, name + ".png")

        if output_path == filepath:
            print(f"Skipping '{filename}' - already in PNG")
            return False

        img.save(output_path, "PNG")
        print(f"Converted '{filename}' to '{output_path}'")

        # Delete the original file (replacement)
        try:
            os.remove(filepath)
            print(f"Removed original '{filename}'")
        except OSError as e:
            print(f"Error deleting '{filename}': {e}")

        return True

    except Exception as e:
        print(f"Error processing '{filepath}': {e}")
        return False


def convert_textures(directory, progress_callback, start_progress_callback, end_progress_callback, lock):
    """Converts all textures in a directory to PNG format."""

    if not os.path.isdir(directory):
        print(f"Error: '{directory}' is not a valid directory.")
        return

    all_files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f)) and is_image_file(f)]
    total_files = len(all_files)
    processed_count = 0
    output_dir = directory  # output is in the same folder

    start_progress_callback(total_files)

    for filename in all_files:
        filepath = os.path.join(directory, filename)
        if convert_texture_to_png(filepath, output_dir, lock):
            pass  # Successfully converted

        processed_count += 1
        progress_callback(processed_count)

    end_progress_callback()


# --- GUI Setup ---
root = tk.Tk()
root.title("Texture Batch Converter")
root.geometry("600x350")

# --- Styling ---
style = ttk.Style(root)
style.theme_use('clam')

# Font
font_name = "Bahnschrift"

# Color scheme
bg_color = '#2e2e2e'
fg_color = 'white'
text_color = '#d3d3d3'
button_bg_color = '#4a4a4a'
entry_bg_color = "#4a4a4a"
button_active_bg_color = '#606060'

# Configure styles
style.configure('.', background=bg_color, foreground=fg_color, font=(font_name, 10))
style.configure('TLabel', background=bg_color, foreground=fg_color, padding=5, font=(font_name, 12))
style.configure('TButton', background=button_bg_color, foreground=fg_color, padding=8, relief='flat',
                font=(font_name, 11),
                borderwidth=0, focuscolor='gray',
                activebackground=button_active_bg_color, activeforeground=fg_color)
style.map('TButton',
          background=[('active', button_active_bg_color), ('disabled', button_bg_color)],
          foreground=[('disabled', 'gray')])
style.configure('TCombobox', selectbackground=button_bg_color, fieldbackground=button_bg_color,
                background=button_bg_color, foreground=text_color,
                arrowcolor=fg_color, borderwidth=0, lightcolor=button_bg_color, darkcolor=button_bg_color,
                font=(font_name, 11))  # style of ComboBox

style.map('TCombobox', fieldbackground=[('readonly', entry_bg_color)])

style.configure('TEntry', fieldbackground="#4a4a4a", foreground=text_color, font=(font_name, 11))

style.configure('Horizontal.TProgressbar', troughcolor=button_bg_color, background=fg_color)

# --- Main Frame ---
main_frame = ttk.Frame(root, padding=20)
main_frame.pack(expand=True, fill='both')

# --- Folder Selection ---
folder_label = ttk.Label(main_frame, text="Folder:")
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

# --- Quality Selection ---
quality_label = ttk.Label(main_frame, text="Quality Preset:")
quality_label.pack(pady=(10, 5), fill='x')

quality_values_list = ["Very Low", "Low", "Medium", "High"]
quality_combobox = ttk.Combobox(main_frame, values=quality_values_list, state="readonly")
quality_combobox.set("Medium")
quality_combobox.pack(pady=(0, 10), fill='x')

# --- Progress Bar ---
progress_bar = ttk.Progressbar(main_frame, orient="horizontal", length=400, mode="determinate")
progress_bar.pack(pady=(10, 15), fill='x')

# --- Compression Button ---
# Create a thread lock
thread_lock = threading.Lock()


def start_compression():
    directory = folder_path_entry.get()
    if not directory:
        messagebox.showerror("Error", "Please select a folder.")
        return

    # Disable the button and other controls
    compress_button["state"] = "disabled"
    browse_button["state"] = "disabled"
    quality_combobox["state"] = "disabled"

    # Update the progress bar
    def update_progress(value):
        progress_bar["value"] = value
        root.update_idletasks()

    def start_progress(max_value):
        progress_bar["maximum"] = max_value
        progress_bar["value"] = 0

    def end_progress():
        progress_bar["value"] = 0
        messagebox.showinfo("Info", "Texture conversion complete!")
        # Re-enable controls here as well
        compress_button["state"] = "normal"
        browse_button["state"] = "normal"
        quality_combobox["state"] = "readonly"

    # Start the conversion in a separate thread
    threading.Thread(target=lambda: convert_textures(
        directory,
        progress_callback=update_progress,
        start_progress_callback=start_progress,
        end_progress_callback=end_progress,
        lock=thread_lock
    ), daemon=True).start()


compress_button = ttk.Button(main_frame, text="Convert Textures", command=start_compression)
compress_button.pack(pady=(15, 0), fill='x')

# --- Run the GUI ---
root.mainloop()
