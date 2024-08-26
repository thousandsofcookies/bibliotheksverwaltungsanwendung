import sqlite3
import random
from faker import Faker

# Verwenden Sie die Faker-Bibliothek, um zufällige Daten zu generieren
fake = Faker()

def add_many_books(n=10000):
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()

    genres = ["Fantasy", "Science Fiction", "Dystopie", "Romanze", "Thriller", "Krimi", "Historisch", "Abenteuer", "Philosophie", "Kinderliteratur"]
    statuses = ["Verfügbar", "Ausgeliehen"]

    books = []

    for _ in range(n):
        title = fake.sentence(nb_words=3).strip('.')
        author = fake.name()
        year = fake.date_between(start_date='-100y', end_date='today').strftime('%Y-%m-%d')
        genre = random.choice(genres)
        status = random.choice(statuses)
        books.append((title, author, year, genre, status))

    cursor.executemany("""
        INSERT INTO books (title, author, year, genre, status)
        VALUES (?, ?, ?, ?, ?)
    """, books)

    conn.commit()
    conn.close()

    print(f"{n} Bücher erfolgreich zur Datenbank hinzugefügt.")

# Aufruf der Funktion zum Hinzufügen von 10.000 Büchern
add_many_books(10000)