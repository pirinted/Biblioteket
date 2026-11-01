import sqlite3
from datetime import datetime

conn = sqlite3.connect('bibliotek.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS Books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    author TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT,
    last_name TEXT,
    birth_date TEXT,
    p_number TEXT,
    age INTEGER
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Loans (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    book_id INTEGER,
    FOREIGN KEY(user_id) REFERENCES Users(id),
    FOREIGN KEY(book_id) REFERENCES Books(id)
)
''')
conn.commit()

class Book:
    def __init__(self, title, author):
        self.title = title
        self.author = author

cursor.execute("SELECT COUNT(*) FROM Books")
if cursor.fetchone()[0] == 0:
    books_to_add = [
        Book("Positiv specialpedagogik : teorier och tillämpningar", "Ann-Katrin Swärd, Monica Reichenberg & Siw Fischbein"),
        Book("Varför har ingen berättat det här för mig?", "Julie Smith"),
        Book("Inkluderingskompetens vid adhd & autism", "Linda Jensen"),
        Book("Hantera, utvärdera och förändra: Med lågaffektivt bemötande och tydliggöra", "Bo Hejslöv Elvén & Anna Sjölund"),
        Book("Autistens överlevnadsguide till skolan", "Alexander Skytte & Jiang Millington")
    ]
    for b in books_to_add:
        cursor.execute("INSERT INTO Books (title, author) VALUES (?, ?)", (b.title, b.author))
    conn.commit()
    print("5 böcker har lagts till i databasen!")
