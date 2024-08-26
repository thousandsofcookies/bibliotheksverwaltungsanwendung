import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry  # Import für DateEntry
import database as db

def create_add_tab(parent):
    add_tab = ttk.Frame(parent)
    parent.add(add_tab, text="Hinzufügen")

    vars = create_form(add_tab)
    
    # Speichern-Button mit Icon
    save_icon = tk.PhotoImage(file="save.png")
    add_button = tk.Button(add_tab, text=" Buch hinzufügen", image=save_icon, compound="left", command=lambda: add_book(vars))
    add_button.grid(row=6, column=0, columnspan=2, pady=10)

    # Speicherung des Icons, damit es nicht vom Garbage Collector entfernt wird
    add_tab.save_icon = save_icon

def add_book(vars):
    db.add_book(vars["Titel:"].get(), vars["Autor:"].get(), vars["Erscheinungsjahr:"].get(), 
                vars["Genre:"].get(), vars["Status:"].get())
    clear_form(vars)
    messagebox.showinfo("Erfolg", "Buch erfolgreich hinzugefügt.")

def create_form(tab):
    labels = ["Titel:", "Autor:", "Erscheinungsjahr:", "Genre:", "Status:"]
    vars = {}

    for i, label in enumerate(labels):
        tk.Label(tab, text=label).grid(row=i, column=0)
        if label == "Erscheinungsjahr:":
            var = tk.StringVar()
            date_entry = DateEntry(tab, textvariable=var, date_pattern='yyyy-mm-dd')  # DateEntry hinzufügen
            date_entry.grid(row=i, column=1)
        elif label == "Status:":
            var = tk.StringVar(value="Verfügbar")  # Standardwert festlegen
            status_menu = ttk.OptionMenu(tab, var, "Verfügbar", "Verfügbar", "Ausgeliehen")  # Dropdown-Menu erstellen
            status_menu.grid(row=i, column=1)
        else:
            var = tk.StringVar()
            tk.Entry(tab, textvariable=var).grid(row=i, column=1)
        vars[label] = var

    return vars

def clear_form(vars):
    for var in vars.values():
        var.set("")