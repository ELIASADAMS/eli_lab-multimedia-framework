import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os

class DocumentationGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Project Documentation Generator")

        # --- Style Configuration ---
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
        style.configure('TLabel', background=bg_color, foreground=fg_color, padding=10, font=(font_name, 12, 'bold'))
        style.configure('TButton', background=button_bg_color, foreground=fg_color, padding=8, relief='flat',
                        font=(font_name, 11), borderwidth=0, focuscolor='gray',
                        activebackground=button_active_bg_color, activeforeground=fg_color)
        style.map('TButton',
                  background=[('active', button_active_bg_color), ('disabled', button_bg_color)],
                  foreground=[('disabled', 'gray')])
        style.configure('TEntry', fieldbackground=entry_bg_color, foreground=text_color, font=(font_name, 11))

        # --- GUI Elements ---
        main_frame = ttk.Frame(root, padding=20)
        main_frame.pack(expand=True, fill='both')

        # Project Directory Selection
        ttk.Label(main_frame, text="Project Directory:").grid(row=0, column=0, padx=10, pady=5, sticky='w')
        self.directory_entry = ttk.Entry(main_frame, width=50)
        self.directory_entry.grid(row=0, column=1, padx=10, pady=5)
        self.browse_button = ttk.Button(main_frame, text="Browse", command=self.browse_directory)
        self.browse_button.grid(row=0, column=2, padx=10, pady=5)

        # Labels and Entry fields
        ttk.Label(main_frame, text="Project Title:").grid(row=1, column=0, padx=10, pady=5, sticky='w')
        self.title_entry = ttk.Entry(main_frame, width=50)
        self.title_entry.grid(row=1, column=1, padx=10, pady=5)

        ttk.Label(main_frame, text="Project Description:").grid(row=2, column=0, padx=10, pady=5, sticky='w')
        self.description_entry = ttk.Entry(main_frame, width=50)
        self.description_entry.grid(row=2, column=1, padx=10, pady=5)

        ttk.Label(main_frame, text="Authors (comma-separated):").grid(row=3, column=0, padx=10, pady=5, sticky='w')
        self.authors_entry = ttk.Entry(main_frame, width=50)
        self.authors_entry.grid(row=3, column=1, padx=10, pady=5)

        ttk.Label(main_frame, text="Timeline:").grid(row=4, column=0, padx=10, pady=5, sticky='w')
        self.timeline_entry = ttk.Entry(main_frame, width=50)
        self.timeline_entry.grid(row=4, column=1, padx=10, pady=5)

        ttk.Label(main_frame, text="Assets (populated from folder):").grid(row=5, column=0, padx=10, pady=5, sticky='w')
        self.assets_listbox = tk.Listbox(main_frame, selectmode=tk.MULTIPLE, width=50)
        self.assets_listbox.grid(row=5, column=1, padx=10, pady=5)

        # Button to generate documentation
        self.generate_button = ttk.Button(main_frame, text="Generate Documentation", command=self.generate_documentation)
        self.generate_button.grid(row=6, column=1, padx=10, pady=5)

        # Text area to display documentation
        self.documentation_text = tk.Text(main_frame, wrap=tk.WORD, width=60, height=15)
        self.documentation_text.grid(row=7, column=0, columnspan=3, padx=10, pady=5)

        # Button to save documentation
        self.save_button = ttk.Button(main_frame, text="Save Documentation", command=self.save_documentation)
        self.save_button.grid(row=8, column=1, padx=10, pady=5)

    def browse_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.directory_entry.delete(0, tk.END)
            self.directory_entry.insert(0, directory)
            self.populate_assets(directory)

    def populate_assets(self, directory):
        self.assets_listbox.delete(0, tk.END)  # Clear current list
        try:
            for filename in os.listdir(directory):
                if os.path.isfile(os.path.join(directory, filename)):
                    self.assets_listbox.insert(tk.END, filename)
        except Exception as e:
            messagebox.showerror("Error", f"Could not list assets: {e}")

    def generate_documentation(self):
        title = self.title_entry.get()
        description = self.description_entry.get()
        authors = self.authors_entry.get()
        timeline = self.timeline_entry.get()
        selected_assets = [self.assets_listbox.get(i) for i in self.assets_listbox.curselection()]

        if not title or not description or not authors:
            messagebox.showwarning("Warning", "Please fill in all fields.")
            return

        documentation = f"# {title}\n\n## Description\n{description}\n\n## Authors\n{authors}\n\n## Timeline\n{timeline}\n\n## Assets\n"
        documentation += "\n".join(selected_assets) if selected_assets else "No assets selected."

        self.documentation_text.delete(1.0, tk.END)
        self.documentation_text.insert(tk.END, documentation)

    def save_documentation(self):
        documentation = self.documentation_text.get(1.0, tk.END).strip()
        if not documentation:
            messagebox.showwarning("Warning", "There is no documentation to save.")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".md",
                                                 filetypes=[("Markdown Files", "*.md"), ("Text Files", "*.txt")])
        if file_path:
            try:
                with open(file_path, 'w') as file:
                    file.write(documentation)
                messagebox.showinfo("Success", "Documentation saved successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Could not save documentation: {e}")

    if __name__ == "__main__":
        root = tk.Tk()
        app = DocumentationGenerator(root)
        root.mainloop()
