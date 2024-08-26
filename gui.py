import tkinter as tk
from tkinter import ttk
import search
import add

class LibraryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Bibliotheksverwaltung")

        self.tab_control = ttk.Notebook(root)
        self.tab_control.pack(expand=1, fill="both")

        # Tabs erstellen
        search.create_search_tab(self.tab_control)
        add.create_add_tab(self.tab_control)

def run_app():
    root = tk.Tk()
    app = LibraryApp(root)
    root.mainloop()