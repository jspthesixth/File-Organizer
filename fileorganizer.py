import os
import shutil
# import ctypes -> See comments; lines 8-13
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox

"""OS: Windows
Setting DPI awareness mode to support DPI scaling.
Long story short, to remove blury text from GUI on high resolution displays.
ctypes.windll.shcore.SetProcessDpiAwareness(1)
Include the line above, line 14 and import 'ctypes' library, line 3
"""

class FileOrganizer(Tk):
    def __init__(self):
        super().__init__()
        self.geometry("400x400")
        self.title("FileOrganizer")
        
        self.label1_frame = ttk.LabelFrame(self, text="Select folder:")
        self.label1_frame.grid(column=0, row=0, padx=10, pady=10, sticky=W)
        self.label2_frame = ttk.LabelFrame(self, text="Select destination folder:")
        self.label2_frame.grid(column=0, row=3, padx=10, pady=10, sticky=W)
        self.label3_frame = ttk.LabelFrame(self, text="Select extension of files you want to copy or move:")
        self.label3_frame.grid(column=0, row=1, padx=10, pady=10, sticky=W)
        self.label4_frame = ttk.LabelFrame(self, text="Select a process action:")
        self.label4_frame.grid(column=0, row=2, padx=10, pady=10, sticky=W)

        self.select_initial()
        self.select_destination()
        self.select_extension()
        self.select_action()
        self.start_button()
        self.quit_button()

    def initial_directory(self):
        self.extensions = []
        self.initial_dir = filedialog.askdirectory(initialdir="/")
        self.label1 = ttk.Label(self.label1_frame, text="")
        self.label1.grid(column=0, row=2, sticky=W)
        self.label1.configure(text=self.initial_dir)
        try:
            for file in os.listdir(self.initial_dir):
                root, ext = os.path.splitext(file)
                ext = ext[1:]
                fullpath = os.path.join(self.initial_dir, file)
                if ext.lower() not in self.extensions and os.path.isfile(fullpath):
                    self.extensions.append(ext.lower())
        except FileNotFoundError:
            self.label1.configure(text="My brain huuuurts!")
        else:
            self.select_ext['values'] = self.extensions
            self.select_ext['state'] = "readonly"
            self.select2['state'] = "!disabled"

    def select_initial(self):
        self.select1 = ttk.Button(self.label1_frame, text="Select", command=self.initial_directory)
        self.select1.grid(column=0, row=1, sticky=W)

    def select_extension(self):
        self.extension = StringVar()
        self.select_ext = ttk.Combobox(self.label3_frame, textvariable=self.extension, state="disabled")
        self.select_ext.grid(column=0, row=2, sticky=W)

    def select_action(self):
        self.action = StringVar()
        self.copy = ttk.Radiobutton(self.label4_frame, text="Copy", variable=self.action, value="copy")
        self.copy.grid(column=0, row=3, sticky=W)
        self.move = ttk.Radiobutton(self.label4_frame, text="Move", variable=self.action, value="move")
        self.move.grid(column=0, row=4, sticky=W)

    def destination_directory(self):
        self.destination_dir = filedialog.askdirectory(initialdir="/")
        self.label2 = ttk.Label(self.label2_frame, text="")
        self.label2.grid(column=0, row=6, sticky=W)
        self.label2.configure(text=self.destination_dir)
        self.start_btn['state'] = "!disabled"

    def select_destination(self):
        self.select2 = ttk.Button(self.label2_frame, text="Select", state="disabled", command=self.destination_directory)
        self.select2.grid(column=0, row=5, sticky=W)

    def start(self):
        if self.action.get() == "copy":
            for file in os.listdir(self.initial_dir):
                root, ext = os.path.splitext(file)
                ext = ext[1:]
                fullpath = os.path.join(self.initial_dir, file)
                if ext.lower() == self.extension.get() and os.path.isfile(fullpath):
                    shutil.copy(fullpath, self.destination_dir)

        elif self.action.get() == "move":
            for file in os.listdir(self.initial_dir):
                root, ext = os.path.splitext(file)
                ext = ext[1:]
                fullpath = os.path.join(self.initial_dir, file)
                # shutil.move() won't overwrite files with the same name and it doesn't have to...for your safety
                # "Please. This is supposed to be a happy occasion. Let's not bicker and argue over who killed who."
                if file in os.listdir(self.destination_dir):
                    continue
                elif ext.lower() == self.extension.get() and os.path.isfile(fullpath):
                    shutil.move(fullpath, self.destination_dir)

        # Resetting everything for a rerun
        self.label1['text'] = ""
        self.label2['text'] = ""
        self.action.set("")
        self.extension.set("")
        self.select_ext['state'] = "disabled"
        self.select2['state'] = "disabled"
        self.start_btn['state'] = "disabled"
        messagebox.showinfo("FileOrganizer", "Process is done!")

    def start_button(self):
        self.start_btn = ttk.Button(self, text="Start", state="disabled", command=self.start)
        self.start_btn.grid(column=0, row=7, padx=10, pady=5, sticky=W)

    def quit_app(self):
        self.destroy()

    def quit_button(self):
        self.quit_btn = ttk.Button(self, text="Quit", command=self.quit_app)
        self.quit_btn.grid(column=0, row=8, padx=10, sticky=W)

if __name__ == "__main__":
    try:
        application = FileOrganizer()
        application.mainloop()
    except TclError:
        if os.environ.get("DISPLAY", "") == "":
            os.environ.__setitem__("DISPLAY", ":1.0")
        application = FileOrganizer()
        application.mainloop()
