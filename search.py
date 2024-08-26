import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry  # Import für DateEntry
import sqlite3  # Für die Datenbankverbindung
import database as db

# Funktion für die allgemeine Suche nach Büchern
def search_books(search_var, tree):
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()

    # Suchbegriff für allgemeine Suche
    query = f"%{search_var.get()}%"
    cursor.execute("SELECT * FROM books WHERE title LIKE ? OR author LIKE ?", (query, query))
    result = cursor.fetchall()

    # Löschen Sie alle vorhandenen Einträge in der Treeview
    for item in tree.get_children():
        tree.delete(item)

    # Fügen Sie die gefundenen Bücher zur Treeview hinzu
    for row in result:
        tree.insert("", "end", values=row)

    conn.close()

# Funktion für die spezifische Suche nach einem Buch anhand seiner ID
def search_book_by_id(book_id):
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM books WHERE id=?", (book_id,))
    result = cursor.fetchall()

    conn.close()
    return result

# Funktion zum Erstellen des Such-Tabs
def create_search_tab(parent):
    search_tab = ttk.Frame(parent)
    parent.add(search_tab, text="Suchen")

    # Frame für die Suchleiste und Buttons
    search_frame = tk.Frame(search_tab)
    search_frame.grid(row=0, column=0, padx=5, pady=5, sticky='w')

    search_label = tk.Label(search_frame, text="Suchbegriff:")
    search_label.grid(row=0, column=0)
    
    search_var = tk.StringVar()
    search_entry = tk.Entry(search_frame, textvariable=search_var)
    search_entry.grid(row=0, column=1, padx=5)

    # Such-Button mit Icon
    search_icon = tk.PhotoImage(file="search.png")
    search_button = tk.Button(search_frame, text=" Suchen", image=search_icon, compound="left", command=lambda: search_books(search_var, tree))
    search_button.grid(row=0, column=2, padx=5)

    # Buttons für Bearbeiten und Löschen mit Symbolen
    edit_icon = tk.PhotoImage(file="edit.png")  # Verwenden Sie das entsprechende Symbolbild
    delete_icon = tk.PhotoImage(file="delete.png")  # Verwenden Sie das entsprechende Symbolbild

    edit_button = tk.Button(search_frame, text=" Bearbeiten", image=edit_icon, compound="left", state=tk.DISABLED, command=lambda: open_edit_modal(tree))
    edit_button.grid(row=0, column=3, padx=5)

    delete_button = tk.Button(search_frame, text=" Löschen", image=delete_icon, compound="left", state=tk.DISABLED, command=lambda: confirm_delete(tree))
    delete_button.grid(row=0, column=4, padx=5)

    # Treeview Widget für tabellarische Ansicht
    columns = ("ID", "Titel", "Autor", "Erscheinungsjahr", "Genre", "Status")
    tree = ttk.Treeview(search_tab, columns=columns, show='headings')
    tree.heading("ID", text="ID")
    tree.heading("Titel", text="Titel")
    tree.heading("Autor", text="Autor")
    tree.heading("Erscheinungsjahr", text="Erscheinungsjahr")
    tree.heading("Genre", text="Genre")
    tree.heading("Status", text="Status")

    # Spaltenbreite festlegen
    for col in columns:
        tree.column(col, width=100, anchor=tk.CENTER)

    tree.grid(row=1, column=0, columnspan=5, sticky='nsew')

    # Scrollbar hinzufügen
    scrollbar = ttk.Scrollbar(search_tab, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.grid(row=1, column=5, sticky='ns')

    search_tab.grid_rowconfigure(1, weight=1)
    search_tab.grid_columnconfigure(1, weight=1)

    # Ereignisbindung, um die Buttons zu aktivieren, wenn eine Zeile ausgewählt wird
    tree.bind("<<TreeviewSelect>>", lambda event: on_tree_select(event, edit_button, delete_button))

    # Speicherung der Symbole, damit sie nicht vom Garbage Collector entfernt werden
    search_button.image = search_icon
    edit_button.image = edit_icon
    delete_button.image = delete_icon

# Funktion zur Aktivierung der Buttons, wenn eine Zeile ausgewählt wird
def on_tree_select(event, edit_button, delete_button):
    selected_item = event.widget.selection()
    if selected_item:
        edit_button.config(state=tk.NORMAL)
        delete_button.config(state=tk.NORMAL)
    else:
        edit_button.config(state=tk.DISABLED)
        delete_button.config(state=tk.DISABLED)

# Funktion zum Öffnen des Bearbeitungsfensters
def open_edit_modal(tree):
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Fehler", "Kein Buch ausgewählt.")
        return

    book_id = tree.item(selected_item, "values")[0]
    print(f"DEBUG: Ausgewählte Buch-ID: {book_id}")  # Debugging-Ausgabe

    # Verwenden der spezifischen Suchfunktion nach ID
    book = search_book_by_id(str(book_id))
    print(f"DEBUG: Gefundenes Buch: {book}")  # Debugging-Ausgabe

    if not book or len(book) == 0:
        messagebox.showerror("Fehler", f"Das ausgewählte Buch mit der ID {book_id} existiert nicht mehr.")
        return

    book = book[0]  # Nur das erste Ergebnis verwenden

    edit_window = tk.Toplevel()
    edit_window.title("Buch bearbeiten")
    edit_window.geometry("400x300")

    vars = {}

    labels = ["Titel", "Autor", "Erscheinungsjahr", "Genre", "Status"]
    for i, label in enumerate(labels):
        tk.Label(edit_window, text=label).grid(row=i, column=0, padx=5, pady=5)

        if label == "Erscheinungsjahr":
            var = tk.StringVar(value=book[i + 1])
            date_entry = DateEntry(edit_window, textvariable=var, date_pattern='yyyy-mm-dd')
            date_entry.grid(row=i, column=1, padx=5, pady=5)
        elif label == "Status":
            var = tk.StringVar(value=book[i + 1])
            status_menu = ttk.OptionMenu(edit_window, var, book[i + 1], "Verfügbar", "Ausgeliehen")
            status_menu.grid(row=i, column=1, padx=5, pady=5)
        else:
            var = tk.StringVar(value=book[i + 1])
            tk.Entry(edit_window, textvariable=var).grid(row=i, column=1, padx=5, pady=5)

        vars[label] = var

    tk.Button(edit_window, text="Speichern", command=lambda: save_edit(book_id, vars, edit_window)).grid(row=5, column=0, columnspan=2, pady=10)
    tk.Button(edit_window, text="Abbrechen", command=edit_window.destroy).grid(row=6, column=0, columnspan=2)

# Funktion zum Speichern der bearbeiteten Daten
def save_edit(book_id, vars, window):
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE books
        SET title=?, author=?, year=?, genre=?, status=?
        WHERE id=?
    """, (vars["Titel"].get(), vars["Autor"].get(), vars["Erscheinungsjahr"].get(),
          vars["Genre"].get(), vars["Status"].get(), book_id))

    conn.commit()
    conn.close()

    messagebox.showinfo("Erfolg", "Buch erfolgreich bearbeitet.")
    window.destroy()

# Funktion zur Bestätigung des Löschvorgangs
def confirm_delete(tree):
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Fehler", "Kein Buch ausgewählt.")
        return

    book_id = tree.item(selected_item, "values")[0]

    response = messagebox.askyesno("Buch löschen", "Sind Sie sicher, dass Sie dieses Buch löschen möchten?")
    if response:
        conn = sqlite3.connect('library.db')
        cursor = conn.cursor()

        cursor.execute("DELETE FROM books WHERE id=?", (book_id,))
        conn.commit()
        conn.close()

        tree.delete(selected_item)  # Zeile aus der Tabelle entfernen
        messagebox.showinfo("Erfolg", "Buch erfolgreich gelöscht.")