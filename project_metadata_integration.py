import json
import os
import tkinter as tk
import tkinter.messagebox
import tkinter.ttk as ttk
from tkinter import filedialog


class MetadataForm(ttk.Frame):
    """form for entering and saving project metadata"""

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self.metadata_dir = None  # Initialize metadata
        self.metadata_file_path = None  # Initialize path

        self.load_style()
        self.init_ui()

    def load_style(self):
        # Load the style
        style = ttk.Style()
        style.theme_use('clam')
        # Font and Colors
        font_name = "Bahnschrift"
        bg_color = '#2e2e2e'
        fg_color = 'white'
        entry_bg_color = "#4a4a4a"
        button_bg_color = '#4a4a4a'
        button_active_bg_color = '#606060'
        text_color = '#d3d3d3'

        # Configure Styles
        style.configure('.', background=bg_color, foreground=fg_color, font=(font_name, 10))
        style.configure('TLabel', background=bg_color, foreground=fg_color, padding=5, font=(font_name, 12))
        style.configure('TButton', background=button_bg_color, foreground=fg_color, padding=8, relief='flat',
                        font=(font_name, 11),
                        borderwidth=0, focuscolor='gray',
                        activebackground=button_active_bg_color, activeforeground=fg_color)
        style.map('TButton',
                  background=[('active', button_active_bg_color), ('disabled', button_bg_color)],
                  foreground=[('disabled', 'gray')])
        style.configure('TEntry', fieldbackground=entry_bg_color, foreground=text_color, font=(font_name, 11))

        self.style = style

    def init_ui(self):
        """UI elements"""

        self.project_name = tk.StringVar()
        self.project_code = tk.StringVar()
        self.client = tk.StringVar()
        self.pipeline_version = tk.StringVar()
        self.lead_artist = tk.StringVar()
        self.project_description = tk.StringVar()

        # Labels and Entry Fields
        ttk.Label(self, text="Project Name:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        ttk.Entry(self, textvariable=self.project_name, width=40).grid(row=0, column=1, sticky="ew", padx=5, pady=5)

        ttk.Label(self, text="Project Code:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        ttk.Entry(self, textvariable=self.project_code, width=40).grid(row=1, column=1, sticky="ew", padx=5, pady=5)

        ttk.Label(self, text="Client:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        ttk.Entry(self, textvariable=self.client, width=40).grid(row=2, column=1, sticky="ew", padx=5, pady=5)

        ttk.Label(self, text="Pipeline Version:").grid(row=3, column=0, sticky="w", padx=5, pady=5)
        ttk.Entry(self, textvariable=self.pipeline_version, width=40).grid(row=3, column=1, sticky="ew", padx=5, pady=5)

        ttk.Label(self, text="Lead Artist:").grid(row=4, column=0, sticky="w", padx=5, pady=5)
        ttk.Entry(self, textvariable=self.lead_artist, width=40).grid(row=4, column=1, sticky="ew", padx=5, pady=5)

        ttk.Label(self, text="Project Description:").grid(row=5, column=0, sticky="w", padx=5, pady=5)
        self.description_text = tk.Text(self, width=30, height=5, background="#4a4a4a", foreground="#d3d3d3")
        self.description_text.grid(row=5, column=1, sticky="ew", padx=5, pady=5)

        # Buttons
        self.browse_button = ttk.Button(self, text="Select Metadata Directory", command=self.browse_directory)
        self.browse_button.grid(row=6, column=0, sticky="w", padx=5, pady=10)

        self.load_button = ttk.Button(self, text="Load Metadata", command=self.load_metadata,
                                      state="disabled")
        self.load_button.grid(row=6, column=1, sticky="w", padx=5, pady=10)

        self.save_button = ttk.Button(self, text="Save Metadata", command=self.save_metadata)  # Call Save function
        self.save_button.grid(row=6, column=1, sticky="e", padx=5, pady=5)

        #column weights
        self.columnconfigure(1, weight=1)

    def browse_directory(self):
        """set metadata directory."""
        self.metadata_dir = filedialog.askdirectory(title="Select Metadata Directory")
        if self.metadata_dir:
            self.metadata_file_path = os.path.join(self.metadata_dir, "project_metadata.json")
            self.load_button.config(state="normal")  # Enable load button
            print(f"Metadata directory set to: {self.metadata_dir}")  # Debugging
        else:
            self.metadata_file_path = None  # Reset path to None
            self.load_button.config(state="disabled")
            print("No directory selected.")

    def load_metadata(self):
        """Loads existing metadata from the JSON file (if it exists)."""
        if self.metadata_file_path and os.path.exists(self.metadata_file_path):  # Check file_path
            try:
                with open(self.metadata_file_path, "r") as f:
                    metadata = json.load(f)
                self.project_name.set(metadata.get("project_name", ""))
                self.project_code.set(metadata.get("project_code", ""))
                self.client.set(metadata.get("client", ""))
                self.pipeline_version.set(metadata.get("pipeline_version", ""))
                self.lead_artist.set(metadata.get("lead_artist", ""))
                description = metadata.get("project_description", "")
                self.description_text.delete("1.0", tk.END)  # Clear existing text
                self.description_text.insert(tk.END, description)
                tk.messagebox.showinfo("Metadata Load",
                                       f"Successfully loaded metadata from:\n{self.metadata_file_path}")
            except (FileNotFoundError, json.JSONDecodeError):
                tk.messagebox.showerror("Load Error",
                                        "Error loading metadata. The file might be corrupted or not found.")
        else:
            tk.messagebox.showinfo("Metadata Load", "No metadata file found or directory selected.")

    def save_metadata(self):
        """Save to JSON file."""
        if not self.metadata_file_path:
            tk.messagebox.showerror("Save Error", "Please select a metadata directory first.")
            return

        metadata = {
            "project_name": self.project_name.get(),
            "project_code": self.project_code.get(),
            "client": self.client.get(),
            "pipeline_version": self.pipeline_version.get(),
            "lead_artist": self.lead_artist.get(),
            "project_description": self.description_text.get("1.0", tk.END).strip()
        }

        if not metadata["project_name"] or not metadata["project_code"]:
            tk.messagebox.showerror("Error", "Project Name and Project Code are required.")
            return

        try:
            os.makedirs(os.path.dirname(self.metadata_file_path), exist_ok=True)  # Make path if doesn't exist
            with open(self.metadata_file_path, "w") as f:
                json.dump(metadata, f, indent=4)
            tk.messagebox.showinfo("Success", f"Project metadata saved to {self.metadata_file_path}")
        except Exception as e:
            tk.messagebox.showerror("Error", f"Error saving meta: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Project Metadata Integration")
    root.geometry("600x400")

    # Basic styling
    style = ttk.Style()
    style.theme_use('clam')

    main_frame = ttk.Frame(root, padding=20)
    main_frame.pack(expand=True, fill="both")

    # Metadata Form
    metadata_form = MetadataForm(main_frame)  # No metadata_dir passed initially
    metadata_form.pack(expand=True, fill="both")

    root.mainloop()
