import tkinter as tk
from tkinter import filedialog
import customtkinter

class CustomDialog(customtkinter.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Select Location and Name for Virtual Environment")
        self.geometry("500x250")
        self.venv_location = None
        self.venv_name = None

        # Set a custom theme
        customtkinter.set_appearance_mode("dark")  # Available modes: "light", "dark"
        customtkinter.set_default_color_theme("blue")  # Available themes: "blue", "green", "dark-blue"

        # Directory selection
        self.dir_label = customtkinter.CTkLabel(self, text="No directory selected")
        self.dir_label.pack(pady=10)
        self.browse_button = customtkinter.CTkButton(self, text="Browse", command=self.browse_directory)
        self.browse_button.pack()

        # Name entry
        self.name_label = customtkinter.CTkLabel(self, text="Enter the name for the virtual environment:")
        self.name_label.pack(pady=10)
        self.name_entry = customtkinter.CTkEntry(self)
        self.name_entry.pack()

        # Control buttons
        self.button_frame = customtkinter.CTkFrame(self)
        self.button_frame.pack(pady=20)
        self.submit_button = customtkinter.CTkButton(self.button_frame, text="Submit", command=self.submit)
        self.submit_button.pack(side=tk.RIGHT, padx=10)
        self.cancel_button = customtkinter.CTkButton(self.button_frame, text="Cancel", command=self.cancel)
        self.cancel_button.pack(side=tk.RIGHT)

    def browse_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.dir_label.configure(text=directory)
            self.venv_location = directory

    def submit(self):
        if not self.venv_location:
            customtkinter.CTkMessageBox.showerror(self, "Error", "Please select a directory.")
            return
        self.venv_name = self.name_entry.get()
        if not self.venv_name:
            customtkinter.CTkMessageBox.showerror(self, "Error", "Please enter a name for the virtual environment.")
            return
        self.destroy()

    def cancel(self):
        self.venv_location = None
        self.venv_name = None
        self.destroy()

def ask_for_venv_details(parent):
    dialog = CustomDialog(parent)
    parent.wait_window(dialog)
    return dialog.venv_location, dialog.venv_name