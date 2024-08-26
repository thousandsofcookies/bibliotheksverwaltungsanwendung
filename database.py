import sqlite3

def create_connection():
    conn = sqlite3.connect('library.db')
    return conn

def create_table():
    conn = create_connection()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS books (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    author TEXT NOT NULL,
                    year INTEGER NOT NULL,
                    genre TEXT NOT NULL,
                    status TEXT NOT NULL)''')
    conn.commit()
    conn.close()

def add_book(title, author, year, genre, status):
    conn = create_connection()
    c = conn.cursor()
    c.execute('''INSERT INTO books (title, author, year, genre, status) VALUES (?, ?, ?, ?, ?)''',
              (title, author, year, genre, status))
    conn.commit()
    conn.close()

def edit_book(book_id, title, author, year, genre, status):
    conn = create_connection()
    c = conn.cursor()
    c.execute('''UPDATE books SET title = ?, author = ?, year = ?, genre = ?, status = ? WHERE id = ?''',
              (title, author, year, genre, status, book_id))
    conn.commit()
    conn.close()

def delete_book(book_id):
    conn = create_connection()
    c = conn.cursor()
    c.execute('''DELETE FROM books WHERE id = ?''', (book_id,))
    conn.commit()
    conn.close()

def search_books(search_query):
    conn = create_connection()
    c = conn.cursor()
    c.execute('''SELECT * FROM books WHERE title LIKE ? OR author LIKE ? OR genre LIKE ? OR year LIKE ?''',
              ('%' + search_query + '%', '%' + search_query + '%', '%' + search_query + '%', '%' + search_query + '%'))
    rows = c.fetchall()
    conn.close()
    return rows

def get_all_books():
    conn = create_connection()
    c = conn.cursor()
    c.execute('''SELECT * FROM books''')
    rows = c.fetchall()
    conn.close()
    return rows