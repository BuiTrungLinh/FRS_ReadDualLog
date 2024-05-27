import tkinter as tk
import webbrowser
from tkinter.filedialog import askopenfilename

import main
from tkinter import messagebox


class MainGUI:
    def __init__(self):
        self.path_expected_file = None
        self.path_log_file = None

        # Start layout
        self.root = tk.Tk()
        self.root.title('Check_Misread_DualTest')
        self.root.config(bg="skyblue")
        self.root.eval('tk::PlaceWindow . center')
        self.root.resizable(False, False)
        # self.root.geometry("900x800")

        # Create Frame header
        header_frame = tk.Frame(self.root)
        header_frame.grid(row=0, column=0, padx=10, pady=5)
        # Frame header - Title
        label_title = tk.Label(header_frame, text='Check Misread DualTest', font=('Arial', 18))
        label_title.pack(padx=10, pady=10)

        # Frame body
        body_frame = tk.Frame(self.root)
        body_frame.grid(row=1, column=0, padx=10, pady=5)

        self.label_log_file = tk.Label(body_frame, text='Path Log File (.log):', font='Arial 10 bold')
        self.label_log_file.grid(row=0, column=0, padx=5, pady=5)
        self.textbox_log_file = tk.Text(body_frame, height=2, width=50, font=('Arial', 10))
        self.textbox_log_file.grid(row=0, column=1, padx=5, pady=5)

        # open_button = tk.Button(body_frame, text='Open a File', command=self.select_file)
        # open_button.grid(row=0, column=2, padx=5, pady=5)

        self.label_expected_file = tk.Label(body_frame, text='Path Expected File (.txt):', font='Arial 10 bold')
        self.label_expected_file.grid(row=1, column=0, padx=5, pady=5)
        self.textbox_expected_file = tk.Text(body_frame, height=2, width=50, font=('Arial', 10))
        self.textbox_expected_file.grid(row=1, column=1, padx=5, pady=5)

        footer_frame = tk.Frame(self.root)
        footer_frame.grid(row=3, column=0, padx=10, pady=5)
        self.button_execute = tk.Button(footer_frame, text='Execute!', font=('Arial', 18), command=self.execute)
        self.button_execute.grid(row=0, column=0, padx=10, pady=10)
        #
        self.button_refresh = tk.Button(footer_frame, text='Refresh', font=('Arial', 18), command=self.clear)
        self.button_refresh.grid(row=0, column=1, padx=10, pady=10)

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        # show GUI
        self.root.mainloop()

    def execute(self):
        self.path_log_file = self.textbox_log_file.get("1.0", tk.END).strip().replace('"', '')
        self.path_expected_file = self.textbox_expected_file.get("1.0", tk.END).strip('"').replace('"', '')
        if not self.path_log_file or not self.path_expected_file:
            messagebox.showinfo(title='Error_Message', message='Please enter path file!')
            return
        main.process(self.path_log_file, self.path_expected_file)

    def clear(self):
        self.textbox_log_file.delete("1.0", tk.END)
        self.textbox_expected_file.delete("1.0", tk.END)

    def on_closing(self):
        if messagebox.askyesno(title="Quit?", message="Do you really want to quit?"):
            self.root.destroy()

    # def select_file(self):
    #     filetypes = (
    #         ('text files', '*.txt'),
    #         ('All files', '*.*')
    #     )
    #
    #     filenames = askopenfilename(
    #         title='Open a file',
    #         initialdir='/',
    #         filetypes=filetypes)
    #
    #     messagebox.showinfo(title='Selected Files',
    #                         message=filenames)


def start_up():
    MainGUI()


def callback(url):
    webbrowser.open_new(url)


def show_msg(title, content):
    messagebox.showinfo(title=title, message=content)
