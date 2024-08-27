import tkinter as tk  # Importiert das tkinter-Modul für die GUI-Erstellung
from tkinter import ttk, messagebox  # Importiert zusätzliche tkinter-Module für erweiterte Widgets und Nachrichtenboxen
from tkcalendar import DateEntry  # Importiert DateEntry für die Auswahl von Datumsangaben
import database as db  # Importiert ein benutzerdefiniertes Modul für die Datenbankoperationen

def create_add_tab(parent):
    # Erstellt ein neues Tab in der Tab-Ansicht
    add_tab = ttk.Frame(parent)
    parent.add(add_tab, text="Hinzufügen")

    # Erstellt das Formular und speichert die zugehörigen Variablen in einem Dictionary
    vars = create_form(add_tab)
    
    # Erstellt den "Speichern"-Button mit einem Icon
    save_icon = tk.PhotoImage(file="save.png")  # Lädt das Icon für den Button
    add_button = tk.Button(add_tab, text=" Buch hinzufügen", image=save_icon, compound="left", command=lambda: add_book(vars))
    add_button.grid(row=6, column=0, columnspan=2, pady=10)  # Positioniert den Button im Grid-Layout

    # Speichert das Icon in der Tab-Instanz, um sicherzustellen, dass es nicht vom Garbage Collector entfernt wird
    add_tab.save_icon = save_icon

def add_book(vars):
    # Funktion zum Hinzufügen eines Buches in die Datenbank
    db.add_book(vars["Titel:"].get(), vars["Autor:"].get(), vars["Erscheinungsjahr:"].get(), 
                vars["Genre:"].get(), vars["Status:"].get())  # Ruft die Datenbankfunktion zum Hinzufügen des Buches auf
    clear_form(vars)  # Löscht die Eingabefelder nach dem Speichern
    messagebox.showinfo("Erfolg", "Buch erfolgreich hinzugefügt.")  # Zeigt eine Bestätigungsmeldung an

def create_form(tab):
    # Funktion zum Erstellen eines Formulars zur Eingabe von Buchdaten
    labels = ["Titel:", "Autor:", "Erscheinungsjahr:", "Genre:", "Status:"]  # Beschriftungen für die Formularelemente
    vars = {}  # Dictionary zur Speicherung der zugehörigen Variablen

    for i, label in enumerate(labels):
        # Erstellt ein Label für jedes Formularelement
        tk.Label(tab, text=label).grid(row=i, column=0)
        if label == "Erscheinungsjahr:":
            # Fügt ein DateEntry-Feld für das Erscheinungsjahr hinzu
            var = tk.StringVar()
            date_entry = DateEntry(tab, textvariable=var, date_pattern='yyyy-mm-dd')  # DateEntry mit Datumsformat
            date_entry.grid(row=i, column=1)
        elif label == "Status:":
            # Erstellt ein Dropdown-Menü für den Buchstatus
            var = tk.StringVar(value="Verfügbar")  # Standardwert ist "Verfügbar"
            status_menu = ttk.OptionMenu(tab, var, "Verfügbar", "Verfügbar", "Ausgeliehen")  # Dropdown-Optionen
            status_menu.grid(row=i, column=1)
        else:
            # Erstellt ein Standard-Eingabefeld für andere Daten
            var = tk.StringVar()
            tk.Entry(tab, textvariable=var).grid(row=i, column=1)
        vars[label] = var  # Speichert die Variable im Dictionary

    return vars  # Gibt das Dictionary mit den Formularvariablen zurück

def clear_form(vars):
    # Funktion zum Zurücksetzen der Formularfelder
    for var in vars.values():
        var.set("")  # Setzt den Wert jeder Formularvariable auf einen leeren String