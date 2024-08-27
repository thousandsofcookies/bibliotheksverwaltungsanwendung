import tkinter as tk  # Importiert das tkinter-Modul für die GUI-Erstellung
from tkinter import ttk  # Importiert zusätzliche tkinter-Module für erweiterte Widgets
import search  # Importiert das Modul 'search', das vermutlich die Suchfunktionalität enthält
import add  # Importiert das Modul 'add', das vermutlich die Funktionalität zum Hinzufügen von Büchern enthält

class LibraryApp:
    def __init__(self, root):
        # Konstruktor der Klasse LibraryApp, der die Hauptanwendung erstellt
        self.root = root
        self.root.title("Bibliotheksverwaltung")  # Setzt den Titel des Hauptfensters

        # Erstellen eines Notizbuch-Widgets, das Tabs zur Organisation der GUI enthält
        self.tab_control = ttk.Notebook(root)
        self.tab_control.pack(expand=1, fill="both")  # Packt das Notizbuch-Widget, sodass es den verfügbaren Platz ausfüllt

        # Tabs erstellen und hinzufügen
        search.create_search_tab(self.tab_control)  # Erstellt den Tab für die Suchfunktionalität
        add.create_add_tab(self.tab_control)  # Erstellt den Tab zum Hinzufügen von Büchern

def run_app():
    # Funktion zum Starten der Anwendung
    root = tk.Tk()  # Erstellt das Hauptfenster
    app = LibraryApp(root)  # Erstellt eine Instanz der LibraryApp und übergibt das Hauptfenster
    root.mainloop()  # Startet die Haupt-Ereignisschleife der GUI