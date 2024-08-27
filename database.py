import sqlite3  # Importiert das sqlite3-Modul zur Interaktion mit SQLite-Datenbanken

def create_connection():
    # Stellt eine Verbindung zur SQLite-Datenbank 'library.db' her.
    # Wenn die Datei nicht existiert, wird sie automatisch erstellt.
    conn = sqlite3.connect('library.db')
    return conn  # Gibt das Verbindungsobjekt zurück

def create_table():
    # Erstellt die Tabelle 'books' in der Datenbank, falls sie nicht bereits existiert.
    conn = create_connection()  # Stellt eine Verbindung zur Datenbank her
    c = conn.cursor()  # Erstellt einen Cursor, um SQL-Befehle auszuführen
    # Eindeutige ID für jedes Buch, wird automatisch hochgezählt
    # Titel des Buches, darf nicht leer sein
    # Autor des Buches, darf nicht leer sein
    # Erscheinungsjahr des Buches, darf nicht leer sein
    # Genre des Buches, darf nicht leer sein
    # Status des Buches (z.B. verfügbar oder ausgeliehen), darf nicht leer sein
    c.execute('''CREATE TABLE IF NOT EXISTS books (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,  
                    title TEXT NOT NULL,  
                    author TEXT NOT NULL,  
                    year INTEGER NOT NULL,  
                    genre TEXT NOT NULL,  
                    status TEXT NOT NULL)''')  
    conn.commit()  # Speichert die Änderungen in der Datenbank
    conn.close()  # Schließt die Datenbankverbindung

def add_book(title, author, year, genre, status):
    # Fügt ein neues Buch in die Tabelle 'books' ein.
    conn = create_connection()  # Stellt eine Verbindung zur Datenbank her
    c = conn.cursor()  # Erstellt einen Cursor, um SQL-Befehle auszuführen
    c.execute('''INSERT INTO books (title, author, year, genre, status) VALUES (?, ?, ?, ?, ?)''',
              (title, author, year, genre, status))  # Führt das SQL-INSERT-Statement aus, um ein Buch hinzuzufügen
    conn.commit()  # Speichert die Änderungen in der Datenbank
    conn.close()  # Schließt die Datenbankverbindung

def edit_book(book_id, title, author, year, genre, status):
    # Aktualisiert die Informationen eines bestehenden Buches in der Tabelle 'books'.
    conn = create_connection()  # Stellt eine Verbindung zur Datenbank her
    c = conn.cursor()  # Erstellt einen Cursor, um SQL-Befehle auszuführen
    c.execute('''UPDATE books SET title = ?, author = ?, year = ?, genre = ?, status = ? WHERE id = ?''',
              (title, author, year, genre, status, book_id))  # Führt das SQL-UPDATE-Statement aus, um die Buchdaten zu aktualisieren
    conn.commit()  # Speichert die Änderungen in der Datenbank
    conn.close()  # Schließt die Datenbankverbindung

def delete_book(book_id):
    # Löscht ein Buch aus der Tabelle 'books' basierend auf der übergebenen ID.
    conn = create_connection()  # Stellt eine Verbindung zur Datenbank her
    c = conn.cursor()  # Erstellt einen Cursor, um SQL-Befehle auszuführen
    c.execute('''DELETE FROM books WHERE id = ?''', (book_id,))  # Führt das SQL-DELETE-Statement aus, um das Buch zu löschen
    conn.commit()  # Speichert die Änderungen in der Datenbank
    conn.close()  # Schließt die Datenbankverbindung

def search_books(search_query):
    # Durchsucht die Tabelle 'books' nach Büchern, deren Titel, Autor, Genre oder Jahr dem Suchbegriff entsprechen.
    conn = create_connection()  # Stellt eine Verbindung zur Datenbank her
    c = conn.cursor()  # Erstellt einen Cursor, um SQL-Befehle auszuführen
    c.execute('''SELECT * FROM books WHERE title LIKE ? OR author LIKE ? OR genre LIKE ? OR year LIKE ?''',
              ('%' + search_query + '%', '%' + search_query + '%', '%' + search_query + '%', '%' + search_query + '%'))  # Führt das SQL-SELECT-Statement aus, um nach Büchern zu suchen
    rows = c.fetchall()  # Ruft alle übereinstimmenden Datensätze ab
    conn.close()  # Schließt die Datenbankverbindung
    return rows  # Gibt die Liste der gefundenen Bücher zurück

def get_all_books():
    # Ruft alle Bücher aus der Tabelle 'books' ab.
    conn = create_connection()  # Stellt eine Verbindung zur Datenbank her
    c = conn.cursor()  # Erstellt einen Cursor, um SQL-Befehle auszuführen
    c.execute('''SELECT * FROM books''')  # Führt das SQL-SELECT-Statement aus, um alle Bücher abzurufen
    rows = c.fetchall()  # Ruft alle Datensätze ab
    conn.close()  # Schließt die Datenbankverbindung
    return rows  # Gibt die Liste aller Bücher zurück