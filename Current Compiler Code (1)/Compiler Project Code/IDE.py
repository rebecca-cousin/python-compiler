import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox
from tkinter import filedialog
from functools import partial
import os
import basic

class IDE:
    def __init__(self, root):
        self.root = root
        self.root.title("Group 3 IDE")
        self.file_path = None

        # Text widget for code input
        self.code_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=80, height=20)
        self.code_text.pack(expand=True, fill="both")

        # Text widget for output display
        self.output_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=80, height=10)
        self.output_text.pack(expand=True, fill="both")

        # Menu bar
        menu_bar = tk.Menu(root)
        root.config(menu=menu_bar)

        # File menu
        file_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New", command=self.new_file)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_command(label="Save As", command=self.save_as_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.exit_app)

        # Run menu
        run_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Run", menu=run_menu)
        run_menu.add_command(label="Run Code", command=self.run_code)

        # Compile menu
        compile_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Compile", menu=compile_menu)
        compile_menu.add_command(label="Compile Code", command=self.compile_code)

    def new_file(self):
        self.code_text.delete(1.0, tk.END)
        self.output_text.delete(1.0, tk.END)
        self.file_path = None

    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            self.file_path = file_path
            with open(file_path, "r") as file:
                code = file.read()
                self.code_text.delete(1.0, tk.END)
                self.code_text.insert(tk.END, code)
            self.output_text.delete(1.0, tk.END)

    def save_file(self):
        if self.file_path:
            with open(self.file_path, "w") as file:
                file.write(self.code_text.get(1.0, tk.END))
        else:
            self.save_as_file()

    def save_as_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            self.file_path = file_path
            self.save_file()

    def exit_app(self):
        self.root.destroy()

    def run_code(self):
        code = self.code_text.get(1.0, tk.END).rstrip("\n")
        print("Code to run:", repr(code)) 
        result, error = basic.run("example", code)  # Replace "example" with the filename you want
        self.output_text.delete(1.0, tk.END)
        if error:
            self.output_text.insert(tk.END, f"Runtime Error: {str(error)}")
        else:
            self.output_text.insert(tk.END, f"Output: {str(result)}")

    def compile_code(self):
        code = self.code_text.get(1.0, tk.END)
        _, error = basic.run("example", code)  # Replace "example" with the filename you want
        self.output_text.delete(1.0, tk.END)
        if error:
            self.output_text.insert(tk.END, f"Compile Error: {str(error)}")
        else:
            self.output_text.insert(tk.END, "Compile Successful: No errors found in the code")


if __name__ == "__main__":
    root = tk.Tk()
    ide = IDE(root)
    root.mainloop()


