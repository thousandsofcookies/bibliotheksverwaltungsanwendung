import sqlite3  # Importiert das sqlite3-Modul zur Interaktion mit SQLite-Datenbanken
import random  # Importiert das random-Modul zur Auswahl zufälliger Elemente aus Listen
from faker import Faker  # Importiert die Faker-Bibliothek zur Generierung von Fake-Daten

# Initialisieren der Faker-Bibliothek, um zufällige Daten zu generieren
fake = Faker()

def add_many_books(n=10000):
    # Funktion zum Hinzufügen von 'n' zufälligen Büchern zur Datenbank
    # Standardmäßig werden 10.000 Bücher hinzugefügt, wenn kein Parameter übergeben wird
    
    # Verbindung zur SQLite-Datenbank herstellen
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()  # Erstellen eines Cursors, um SQL-Befehle auszuführen

    # Definieren einer Liste von Genres, aus denen zufällig gewählt wird
    genres = ["Fantasy", "Science Fiction", "Dystopie", "Romanze", "Thriller", "Krimi", "Historisch", "Abenteuer", "Philosophie", "Kinderliteratur"]
    
    # Definieren einer Liste von Statusoptionen
    statuses = ["Verfügbar", "Ausgeliehen"]

    # Leere Liste zur Speicherung der zu generierenden Bücher
    books = []

    # Schleife zur Generierung von 'n' Büchern
    for _ in range(n):
        title = fake.sentence(nb_words=3).strip('.')  # Generiert einen zufälligen Titel mit 3 Wörtern
        author = fake.name()  # Generiert einen zufälligen Autorennamen
        year = fake.date_between(start_date='-100y', end_date='today').strftime('%Y-%m-%d')  # Generiert ein zufälliges Datum in den letzten 100 Jahren
        genre = random.choice(genres)  # Wählt ein zufälliges Genre aus der Liste
        status = random.choice(statuses)  # Wählt zufällig einen Status aus der Liste
        
        # Fügt die generierten Daten als Tupel zur Liste der Bücher hinzu
        books.append((title, author, year, genre, status))

    # Führt eine Masseninsertion der generierten Bücher in die Datenbanktabelle 'books' durch
    cursor.executemany("""
        INSERT INTO books (title, author, year, genre, status)
        VALUES (?, ?, ?, ?, ?)
    """, books)

    # Speichert die Änderungen in der Datenbank
    conn.commit()
    
    # Schließt die Datenbankverbindung
    conn.close()

    # Ausgabe einer Bestätigungsmeldung
    print(f"{n} Bücher erfolgreich zur Datenbank hinzugefügt.")

# Aufruf der Funktion zum Hinzufügen von 10.000 Büchern zur Datenbank
add_many_books(10000)