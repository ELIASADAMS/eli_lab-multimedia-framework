import datetime
import os
import sys
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog, messagebox

import magic


class AdvancedFileRenamer(ttk.Frame):
    """Advanced File Renamer GUI."""

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self.selected_directory = None
        self.file_list = []  # List to store file information
        self.load_style()
        self.init_ui()

    def load_style(self):
        # Load the style
        style = ttk.Style()
        style.theme_use('clam')  # Or try 'alt', 'default'
        # Font and Colors
        font_name = "Bahnschrift"

        bg_color = '#2e2e2e'
        fg_color = 'white'
        entry_bg_color = "#4a4a4a"  # Entry background color
        button_bg_color = '#4a4a4a'
        button_active_bg_color = '#606060'
        text_color = '#d3d3d3'  # Define a text color that is visible
        arrow_color = 'white'

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
        style.configure('TCombobox', selectbackground=button_bg_color, fieldbackground=button_bg_color,
                        background=button_bg_color, foreground=text_color,
                        arrowcolor=fg_color, borderwidth=0, lightcolor=button_bg_color, darkcolor=button_bg_color,
                        font=(font_name, 11))  # style of ComboBox
        style.map('TCombobox', fieldbackground=[('readonly', entry_bg_color)])  # Make it consistent when readonly
        style.configure('Vertical.TScrollbar', background=button_bg_color, arrowcolor=arrow_color, bordercolor=bg_color,
                        troughcolor=bg_color)
        style.configure('Horizontal.TScrollbar', background=button_bg_color, arrowcolor=arrow_color,
                        bordercolor=bg_color, troughcolor=bg_color)

        self.style = style

    def init_ui(self):
        """Initializes the UI elements."""

        # --- Directory Selection ---
        self.dir_label = ttk.Label(self, text="Directory:")
        self.dir_label.grid(row=0, column=0, sticky="w", padx=5, pady=5)

        self.dir_path = tk.StringVar()
        self.dir_entry = ttk.Entry(self, textvariable=self.dir_path, width=50, state="disabled")
        self.dir_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=5)

        self.browse_button = ttk.Button(self, text="Browse", command=self.browse_directory)
        self.browse_button.grid(row=0, column=2, sticky="w", padx=5, pady=5)

        # --- Operation Selection ---
        self.operation_label = ttk.Label(self, text="Operation:")
        self.operation_label.grid(row=1, column=0, sticky="w", padx=5, pady=5)

        self.operation_choices = ["Add Date/Time", "Replace Text", "Insert Text", "Convert Case", "Add Auto-Number",
                                  "Remove Extension", "Change Extension", "Add File Property"]  # operations
        self.operation_variable = tk.StringVar(value=self.operation_choices[0])  # default option
        self.operation_dropdown = ttk.Combobox(self, textvariable=self.operation_variable,
                                               values=self.operation_choices, state="readonly")  # select the operation
        self.operation_dropdown.grid(row=1, column=1, sticky="ew", padx=5, pady=5)
        self.operation_dropdown.bind("<<ComboboxSelected>>", self.operation_selected)

        # --- Operation Parameters (will change based on the selected operation) ---
        self.parameter_frame = ttk.Frame(self)  # Frame to hold operation-specific parameters
        self.parameter_frame.grid(row=2, column=0, columnspan=3, sticky="ew", padx=5, pady=5)

        # --- Preview ---
        self.preview_button = ttk.Button(self, text="Preview", command=self.preview)
        self.preview_button.grid(row=3, column=1, sticky="w", padx=5, pady=5)

        # --- Apply ---
        self.apply_button = ttk.Button(self, text="Apply", command=self.apply, state="disabled")
        self.apply_button.grid(row=3, column=2, sticky="e", padx=5, pady=5)

        # --- File List Display ---
        self.file_list_label = ttk.Label(self, text="Files:")
        self.file_list_label.grid(row=4, column=0, sticky="w", padx=5, pady=5)

        self.file_listbox = tk.Listbox(self, width=70, height=15)  # Display list of the files
        self.file_listbox.grid(row=4, column=1, columnspan=2, sticky="ew", padx=5, pady=5)

        # Configure column weights
        self.columnconfigure(1, weight=1)

    def browse_directory(self):
        """Opens a directory selection dialog."""
        self.selected_directory = filedialog.askdirectory(title="Select Directory")
        if self.selected_directory:
            self.dir_path.set(self.selected_directory)
            self.populate_file_list()

    def populate_file_list(self):
        """Populates the file listbox with files from the selected directory and its subfolders."""
        self.file_listbox.delete(0, tk.END)  # Clears everything to show actual result

        if self.selected_directory:
            self.file_list = []  # Clean last list
            try:
                for root, dirs, files in os.walk(self.selected_directory):
                    for filename in files:
                        filepath = os.path.join(root, filename)
                        self.file_listbox.insert(tk.END, filename)  # Adds to the last line
                        self.file_list.append({"old_name": filename, "new_name": filename,
                                               "filepath": filepath})  # Saves old name and other info
            except Exception as e:
                messagebox.showerror("Error", f"Error reading directory: {e}")

    def operation_selected(self, event=None):
        """Handles the selection of an operation from the dropdown."""
        self.clear_parameter_frame()  # Clean the frame for other selection
        selected_operation = self.operation_variable.get()  # get the selected operation
        if selected_operation == "Add Date/Time":
            self.create_add_datetime_parameters()
        elif selected_operation == "Replace Text":
            self.create_replace_text_parameters()
        elif selected_operation == "Insert Text":
            self.create_insert_text_parameters()
        elif selected_operation == "Convert Case":
            self.create_convert_case_parameters()
        elif selected_operation == "Add Auto-Number":
            self.create_add_autonumber_parameters()
        elif selected_operation == "Remove Extension":
            self.create_remove_extension_parameters()
        elif selected_operation == "Change Extension":
            self.create_change_extension_parameters()
        elif selected_operation == "Add File Property":
            self.create_add_fileproperty_parameters()

    def clear_parameter_frame(self):
        """Clears the parameter frame."""
        for widget in self.parameter_frame.winfo_children():
            widget.destroy()

    def create_add_datetime_parameters(self):
        """Creates parameters for adding date/time."""
        ttk.Label(self.parameter_frame, text="Format:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.datetime_format = tk.StringVar(value="%Y-%m-%d_%H-%M-%S")  # Default value
        ttk.Entry(self.parameter_frame, textvariable=self.datetime_format, width=25).grid(row=0, column=1, sticky="ew",
                                                                                          padx=5, pady=5)

    def create_replace_text_parameters(self):
        """Creates parameters for replacing text."""
        ttk.Label(self.parameter_frame, text="Find:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.replace_find = tk.StringVar()
        ttk.Entry(self.parameter_frame, textvariable=self.replace_find, width=25).grid(row=0, column=1, sticky="ew",
                                                                                       padx=5, pady=5)

        ttk.Label(self.parameter_frame, text="Replace:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.replace_replace = tk.StringVar()
        ttk.Entry(self.parameter_frame, textvariable=self.replace_replace, width=25).grid(row=1, column=1, sticky="ew",
                                                                                          padx=5, pady=5)

    def create_insert_text_parameters(self):
        """Creates parameters for inserting text."""
        ttk.Label(self.parameter_frame, text="Text:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.insert_text = tk.StringVar()
        ttk.Entry(self.parameter_frame, textvariable=self.insert_text, width=25).grid(row=0, column=1, sticky="ew",
                                                                                      padx=5, pady=5)

        ttk.Label(self.parameter_frame, text="Position:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.insert_position = tk.IntVar(value=0)  # Default value
        ttk.Entry(self.parameter_frame, textvariable=self.insert_position, width=10).grid(row=1, column=1, sticky="ew",
                                                                                          padx=5, pady=5)

    def create_convert_case_parameters(self):
        """Creates parameters for converting case."""
        self.case_choices = ["Upper Case", "Lower Case", "Title Case", "Sentence Case"]  # Cases types
        self.case_variable = tk.StringVar(value=self.case_choices[0])  # default case
        ttk.Combobox(self.parameter_frame, textvariable=self.case_variable, values=self.case_choices,
                     state="readonly").grid(row=0, column=1, sticky="ew", padx=5, pady=5)  # Case Dropdown

    def create_add_autonumber_parameters(self):
        """Creates parameters for adding auto-numbering."""
        ttk.Label(self.parameter_frame, text="Start:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.autonumber_start = tk.IntVar(value=1)  # Default
        ttk.Entry(self.parameter_frame, textvariable=self.autonumber_start, width=10).grid(row=0, column=1, sticky="ew",
                                                                                           padx=5, pady=5)

        ttk.Label(self.parameter_frame, text="Step:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.autonumber_step = tk.IntVar(value=1)  # Step default value
        ttk.Entry(self.parameter_frame, textvariable=self.autonumber_step, width=10).grid(row=1, column=1, sticky="ew",
                                                                                          padx=5, pady=5)

        ttk.Label(self.parameter_frame, text="Padding:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.autonumber_padding = tk.IntVar(value=3)  # Padding Default value
        ttk.Entry(self.parameter_frame, textvariable=self.autonumber_padding, width=10).grid(row=2, column=1,
                                                                                             sticky="ew", padx=5,
                                                                                             pady=5)

    def create_remove_extension_parameters(self):
        """Creates parameters for removing extension."""
        # No parameters needed for remove extension
        pass

    def create_change_extension_parameters(self):
        """Creates parameters for changing extension."""
        ttk.Label(self.parameter_frame, text="New Extension:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.new_extension = tk.StringVar(value=".txt")  # Set a default extension
        ttk.Entry(self.parameter_frame, textvariable=self.new_extension, width=10).grid(row=0, column=1, sticky="ew",
                                                                                        padx=5, pady=5)

    def create_add_fileproperty_parameters(self):
        """Creates parameters for adding File Properties."""
        if sys.platform == 'win32':
            properties = ["Name", "Size", "Date Created", "Date Modified", "File Type"]
            self.property_variable = tk.StringVar(value=properties[0])
            ttk.Combobox(self.parameter_frame, textvariable=self.property_variable, values=properties,
                         state="readonly").grid(row=0, column=1, sticky="ew", padx=5, pady=5)

            self.position_choices = ["Prefix", "Suffix"]
            self.position_variable = tk.StringVar(value=self.position_choices[0])
            ttk.Label(self.parameter_frame, text="Position:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
            ttk.Combobox(self.parameter_frame, textvariable=self.position_variable, values=self.position_choices,
                         state="readonly").grid(row=1, column=1, sticky="ew", padx=5, pady=5)
        else:
            ttk.Label(self.parameter_frame, text="Windows-specific feature").grid(row=0, column=0, sticky="w", padx=5,
                                                                                  pady=5)

    def preview(self):
        """Previews the renaming operation."""
        if not self.selected_directory:
            messagebox.showerror("Error", "Please select a directory first.")
            return

        selected_operation = self.operation_variable.get()
        if selected_operation:
            self.apply_button.config(state="normal")  # return it to normal stat

            if selected_operation == "Add Date/Time":
                self.preview_add_datetime()
            elif selected_operation == "Replace Text":
                self.preview_replace_text()
            elif selected_operation == "Insert Text":
                self.preview_insert_text()
            elif selected_operation == "Convert Case":
                self.preview_convert_case()
            elif selected_operation == "Add Auto-Number":
                self.preview_add_autonumber()
            elif selected_operation == "Remove Extension":
                self.preview_remove_extension()
            elif selected_operation == "Change Extension":
                self.preview_change_extension()
            elif selected_operation == "Add File Property":
                self.preview_add_fileproperty()
        else:
            messagebox.showerror("Error", "Please select a function.")
            self.apply_button.config(state="disable")

    def preview_add_datetime(self):
        """Previews adding date/time to filenames."""
        datetime_format = self.datetime_format.get()
        now = datetime.datetime.now().strftime(datetime_format)

        for file_info in self.file_list:
            old_name = file_info["old_name"]
            new_name = f"{now}_{old_name}"
            file_info["new_name"] = new_name

        self.update_file_listbox()

    def preview_replace_text(self):
        """Previews replacing text in filenames."""
        find_text = self.replace_find.get()
        replace_text = self.replace_replace.get()

        for file_info in self.file_list:
            old_name = file_info["old_name"]
            new_name = old_name.replace(find_text, replace_text)
            file_info["new_name"] = new_name

        self.update_file_listbox()

    def preview_insert_text(self):
        """Previews inserting text into filenames."""
        insert_text = self.insert_text.get()
        try:
            insert_position = int(self.insert_position.get())  # Get the int value
        except ValueError:
            messagebox.showerror("Error", "Position must be an integer.")
            return

        for file_info in self.file_list:
            old_name = file_info["old_name"]
            if 0 <= insert_position <= len(old_name):
                new_name = old_name[:insert_position] + insert_text + old_name[
                                                                      insert_position:]  # Insert new text to selected position
                file_info["new_name"] = new_name
            else:
                messagebox.showerror("Error",
                                     f"Invalid position. The position should be between 0 and {len(old_name)}.")
                return

        self.update_file_listbox()

    def preview_convert_case(self):
        """Previews converting the case of filenames."""
        case_type = self.case_variable.get()  # type to convert case
        for file_info in self.file_list:
            old_name = file_info["old_name"]
            if case_type == "Upper Case":
                new_name = old_name.upper()
            elif case_type == "Lower Case":
                new_name = old_name.lower()
            elif case_type == "Title Case":
                new_name = old_name.title()
            elif case_type == "Sentence Case":
                new_name = old_name.capitalize()
            file_info["new_name"] = new_name

        self.update_file_listbox()

    def preview_add_autonumber(self):
        """Previews adding auto-numbering to filenames."""
        try:
            start = int(self.autonumber_start.get())  # start value
            step = int(self.autonumber_step.get())  # step value
            padding = int(self.autonumber_padding.get())  # padding value
        except ValueError:
            messagebox.showerror("Error", "Start, Step, and Padding must be integers.")
            return

        number = start
        for file_info in self.file_list:
            old_name = file_info["old_name"]
            formatted_number = str(number).zfill(padding)  # Pad with leading zeros
            new_name = f"{formatted_number}_{old_name}"  # name with number
            file_info["new_name"] = new_name
            number += step

        self.update_file_listbox()

    def preview_remove_extension(self):
        """Previews removing file extensions from filenames."""
        for file_info in self.file_list:
            old_name = file_info["old_name"]
            name, ext = os.path.splitext(old_name)
            file_info["new_name"] = name

        self.update_file_listbox()

    def preview_change_extension(self):
        """Previews changing file extensions."""
        new_extension = self.new_extension.get()  # get new extension
        for file_info in self.file_list:
            old_name = file_info["old_name"]
            name, ext = os.path.splitext(old_name)  # split the name to get a name and extension

            # Add a dot if the user didn't provide one
            if not new_extension.startswith("."):
                new_extension = "." + new_extension

            new_name = name + new_extension  # new name with new extension
            file_info["new_name"] = new_name

        self.update_file_listbox()

    def preview_add_fileproperty(self):
        """Previews adding the selected file property."""
        if sys.platform == 'win32':
            property_name = self.property_variable.get()
            property_position = self.position_variable.get()
            for file_info in self.file_list:
                old_name = file_info["old_name"]
                filepath = file_info["filepath"]
                try:
                    # Get the property
                    if property_name == "Name":
                        file_property = os.path.basename(filepath)
                    elif property_name == "Size":
                        file_property = str(os.path.getsize(filepath))
                    elif property_name == "Date Created":
                        file_property = datetime.datetime.fromtimestamp(os.path.getctime(filepath)).strftime(
                            "%Y-%m-%d_%H-%M-%S")
                    elif property_name == "Date Modified":
                        file_property = datetime.datetime.fromtimestamp(os.path.getmtime(filepath)).strftime(
                            "%Y-%m-%d_%H-%M-%S")
                    elif property_name == "File Type":
                        file_property = magic.from_file(filepath)

                    # Add the file property to the filename based on position
                    if property_position == "Prefix":
                        new_name = f"{file_property}_{old_name}"
                    elif property_position == "Suffix":
                        new_name = f"{old_name}_{file_property}"
                    file_info["new_name"] = new_name
                except Exception as e:
                    messagebox.showerror("Error", f"Error getting property: {e}")
                    return
            self.update_file_listbox()
        else:
            messagebox.showinfo("Message", "Windows Specific Feature")

    def update_file_listbox(self):
        """Updates the file listbox with the new filenames."""
        self.file_listbox.delete(0, tk.END)  # Clear the listbox
        for file_info in self.file_list:
            self.file_listbox.insert(tk.END, f"{file_info['old_name']} --> {file_info['new_name']}")  # Show result

    def apply(self):
        """Applies the renaming operation to the files."""
        if not self.selected_directory:
            messagebox.showerror("Error", "Please select a directory first.")
            return

        try:
            for file_info in self.file_list:
                old_path = file_info["filepath"]
                new_path = os.path.join(self.selected_directory, file_info["new_name"])
                os.rename(old_path, new_path)

            messagebox.showinfo("Success", "Files renamed successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Error during rename: {e}")
        finally:
            self.populate_file_list()


def integrate_renamer(main_frame):
    renamer = AdvancedFileRenamer(main_frame, padding=10)
    renamer.pack(expand=True, fill="both")


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Advanced File Renamer")
    root.geometry("900x600")

    # Basic styling (replace with your main application's styling)
    style = ttk.Style()
    style.theme_use('clam')

    main_frame = ttk.Frame(root, padding=20)
    main_frame.pack(expand=True, fill="both")

    integrate_renamer(main_frame)

    root.mainloop()
