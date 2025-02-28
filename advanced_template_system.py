import os
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, ttk

class FolderAutomationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Template System")

        self.project_path = tk.StringVar()
        self.project_name = tk.StringVar()
        self.characters = []  # List of character names
        self.locations = {}  # Dictionary of location names and their subfolders
        self.assets = {}  # Dictionary of asset names and their subfolders

        # --- Style Configuration ---
        style = ttk.Style()
        style.theme_use('clam')  # Or try 'alt', 'default'

        # Font and Colors
        font_name = "Bahnschrift"
        bg_color = '#2e2e2e'
        fg_color = 'white'
        entry_bg_color = "#4a4a4a"  # Entry background color
        button_bg_color = '#4a4a4a'
        button_active_bg_color = '#606060'
        text_color = '#d3d3d3' # Define a text color that is visible

        # Configure Styles
        style.configure('.', background=bg_color, foreground=fg_color, font=(font_name, 10))
        style.configure('TLabel', background=bg_color, foreground=fg_color, padding=5, font=(font_name, 12))
        style.configure('TButton', background=button_bg_color, foreground=fg_color, padding=8, relief='flat', font=(font_name, 11),
                        borderwidth=0, focuscolor='gray',
                        activebackground=button_active_bg_color, activeforeground=fg_color)
        style.map('TButton',
                  background=[('active', button_active_bg_color), ('disabled', button_bg_color)],
                  foreground=[('disabled', 'gray')])
        style.configure('TEntry', fieldbackground=entry_bg_color, foreground=text_color, font=(font_name, 11))

        # --- GUI Elements ---
        # Main Frame
        main_frame = ttk.Frame(root, padding=20)
        main_frame.pack(expand=True, fill='both')

        # Project Path
        self.project_path_label = ttk.Label(main_frame, text="Project Path:")
        self.project_path_entry = ttk.Entry(main_frame, textvariable=self.project_path, width=50)
        self.browse_button = ttk.Button(main_frame, text="Browse", command=self.browse_folder)

        # Project Name
        self.project_name_label = ttk.Label(main_frame, text="Project Name:")
        self.project_name_entry = ttk.Entry(main_frame, textvariable=self.project_name, width=50)

        # Characters
        self.characters_label = ttk.Label(main_frame, text="Characters:")
        self.characters_frame = ttk.Frame(main_frame)  # Frame to hold character widgets
        self.add_character_button = ttk.Button(main_frame, text="+ Character", command=self.add_character)

        # Locations
        self.locations_label = ttk.Label(main_frame, text="Locations:")
        self.locations_frame = ttk.Frame(main_frame)  # Frame to hold location widgets
        self.add_location_button = ttk.Button(main_frame, text="+ Location", command=self.add_location)

        # Assets
        self.assets_label = ttk.Label(main_frame, text="Assets:")
        self.assets_frame = ttk.Frame(main_frame)  # Frame to hold asset widgets
        self.add_asset_button = ttk.Button(main_frame, text="+ Asset", command=self.add_asset)

        # Create Button
        self.create_button = ttk.Button(main_frame, text="Create Structure", command=self.create_folders)


        # --- Layout ---
        # Project Path
        self.project_path_label.grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.project_path_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
        self.browse_button.grid(row=0, column=2, sticky="w", padx=5, pady=5)

        # Project Name
        self.project_name_label.grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.project_name_entry.grid(row=1, column=1, sticky="ew", padx=5, pady=5)

        # Characters
        self.characters_label.grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.characters_frame.grid(row=2, column=1, sticky="ew", padx=5, pady=5)
        self.add_character_button.grid(row=2, column=2, sticky="w", padx=5, pady=5)

        # Locations
        self.locations_label.grid(row=3, column=0, sticky="w", padx=5, pady=5)
        self.locations_frame.grid(row=3, column=1, sticky="ew", padx=5, pady=5)
        self.add_location_button.grid(row=3, column=2, sticky="w", padx=5, pady=5)

        # Assets
        self.assets_label.grid(row=4, column=0, sticky="w", padx=5, pady=5)
        self.assets_frame.grid(row=4, column=1, sticky="ew", padx=5, pady=5)
        self.add_asset_button.grid(row=4, column=2, sticky="w", padx=5, pady=5)

        # Create Button
        self.create_button.grid(row=5, column=1, sticky="e", padx=5, pady=10)

        # Column Configuration
        root.columnconfigure(1, weight=1) # Make column 1 expandable

        # Initial Updates
        self.update_character_widgets()
        self.update_location_widgets()
        self.update_asset_widgets()

    def browse_folder(self):
        folder_selected = filedialog.askdirectory()
        self.project_path.set(folder_selected)

    def add_character(self):
        name = simpledialog.askstring("Character Name", "Enter Character Name:")
        if name:
            self.characters.append(name)
            self.update_character_widgets()

    def add_location(self):
        name = simpledialog.askstring("Location Name", "Enter Location Name:")
        if name:
            self.locations[name] = []  # Initialize with an empty list of subfolders
            self.update_location_widgets()

    def add_location_subfolder(self, location_name):
        subfolder_name = simpledialog.askstring("Sub-Location Name", f"Enter Sub-Location Name for {location_name}:")
        if subfolder_name:
            self.locations[location_name].append(subfolder_name)
            self.update_location_widgets()

    def add_asset(self):
        name = simpledialog.askstring("Asset Name", "Enter Asset Name:")
        if name:
            self.assets[name] = []  # Initialize with an empty list of subfolders
            self.update_asset_widgets()

    def add_asset_subfolder(self, asset_name):
        subfolder_name = simpledialog.askstring("Sub-Asset Name", f"Enter Sub-Asset Name for {asset_name}:")
        if subfolder_name:
            self.assets[asset_name].append(subfolder_name)
            self.update_asset_widgets()

    def update_character_widgets(self):
        # Clear existing widgets
        for widget in self.characters_frame.winfo_children():
            widget.destroy()

        # Recreate widgets based on character list
        for i, name in enumerate(self.characters):
            label = tk.Label(self.characters_frame, text=f"{i+1}. {name}")
            label.grid(row=i, column=0, sticky="w", padx=5, pady=2)

            delete_button = tk.Button(self.characters_frame, text="Delete", command=lambda idx=i: self.delete_character(idx))
            delete_button.grid(row=i, column=1, sticky="e", padx=5, pady=2)

    def update_location_widgets(self):
        # Clear existing widgets
        for widget in self.locations_frame.winfo_children():
            widget.destroy()

        row_num = 0
        for location_name, subfolders in self.locations.items():
            label = tk.Label(self.locations_frame, text=f"{location_name}:")
            label.grid(row=row_num, column=0, sticky="w", padx=5, pady=2)

            add_subfolder_button = tk.Button(self.locations_frame, text="+ Add Subfolder", command=lambda name=location_name: self.add_location_subfolder(name))
            add_subfolder_button.grid(row=row_num, column=1, sticky="w", padx=5, pady=2)

            delete_button = tk.Button(self.locations_frame, text="Delete", command=lambda name=location_name: self.delete_location(name))
            delete_button.grid(row=row_num, column=2, sticky="e", padx=5, pady=2)

            # Display subfolders
            for i, subfolder_name in enumerate(subfolders):
                subfolder_label = tk.Label(self.locations_frame, text=f"  - {subfolder_name}")
                subfolder_label.grid(row=row_num + i + 1, column=0, columnspan=3, sticky="w", padx=20, pady=1)  # Indent

            row_num += len(subfolders) + 1  # Increment row_num by the number of subfolders + 1 for the location itself

    def update_asset_widgets(self):
        # Clear existing widgets
        for widget in self.assets_frame.winfo_children():
            widget.destroy()

        row_num = 0
        for asset_name, subfolders in self.assets.items():
            label = tk.Label(self.assets_frame, text=f"{asset_name}:")
            label.grid(row=row_num, column=0, sticky="w", padx=5, pady=2)

            add_subfolder_button = tk.Button(self.assets_frame, text="+ Add Subfolder", command=lambda name=asset_name: self.add_asset_subfolder(name))
            add_subfolder_button.grid(row=row_num, column=1, sticky="w", padx=5, pady=2)

            delete_button = tk.Button(self.assets_frame, text="Delete", command=lambda name=asset_name: self.delete_asset(name))
            delete_button.grid(row=row_num, column=2, sticky="e", padx=5, pady=2)

            # Display subfolders
            for i, subfolder_name in enumerate(subfolders):
                subfolder_label = tk.Label(self.assets_frame, text=f"  - {subfolder_name}")
                subfolder_label.grid(row=row_num + i + 1, column=0, columnspan=3, sticky="w", padx=20, pady=1)  # Indent

            row_num += len(subfolders) + 1  # Increment row_num by the number of subfolders + 1 for the asset itself


    def delete_character(self, index):
        del self.characters[index]
        self.update_character_widgets()

    def delete_location(self, location_name):
        del self.locations[location_name]
        self.update_location_widgets()

    def delete_asset(self, asset_name):
        del self.assets[asset_name]
        self.update_asset_widgets()

    def create_folders(self):
        """Handles the folder creation process."""
        project_path = self.project_path.get()
        project_name = self.project_name.get()

        if not project_path or not project_name:
            messagebox.showerror("Error", "Project Path and Project Name are required.")
            return

        try:
            # Create the core project folder
            core_folder = os.path.join(project_path, project_name)
            os.makedirs(core_folder, exist_ok=True)

            # Create subfolders
            characters_folder = os.path.join(core_folder, f"{project_name}_characters")
            locations_folder = os.path.join(core_folder, f"{project_name}_locations")
            assets_folder = os.path.join(core_folder, f"{project_name}_assets")
            scripts_folder = os.path.join(core_folder, f"{project_name}_scripts")
            misc_folder = os.path.join(core_folder, f"{project_name}_misc")

            os.makedirs(characters_folder, exist_ok=True)
            os.makedirs(locations_folder, exist_ok=True)
            os.makedirs(assets_folder, exist_ok=True)
            os.makedirs(scripts_folder, exist_ok=True)
            os.makedirs(misc_folder, exist_ok=True)

            # Create character folders
            for name in self.characters:
                char_folder = os.path.join(characters_folder, f"{project_name}_{name}")
                os.makedirs(char_folder, exist_ok=True)

            # Create location folders and their subfolders
            for location_name, subfolders in self.locations.items():
                loc_folder = os.path.join(locations_folder, f"{project_name}_{location_name}")
                os.makedirs(loc_folder, exist_ok=True)

                # Create subfolders within the location folder
                for subfolder_name in subfolders:
                    sub_folder_path = os.path.join(loc_folder, f"{project_name}_{subfolder_name}")
                    os.makedirs(sub_folder_path, exist_ok=True)

            # Create assets folders and their subfolders
            for asset_name, subfolders in self.assets.items():
                ass_folder = os.path.join(assets_folder, f"{project_name}_{asset_name}")
                os.makedirs(ass_folder, exist_ok=True)

                # Create subfolders within the location folder
                for subfolder_name in subfolders:
                    sub_folder_path = os.path.join(ass_folder, f"{project_name}_{subfolder_name}")
                    os.makedirs(sub_folder_path, exist_ok=True)

            messagebox.showinfo("Success", "Folders created successfully!")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = FolderAutomationApp(root)
    root.mainloop()