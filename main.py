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


    def register_user():
    print("\n--- Registrera ny användare ---")
    first_name = input("Förnamn: ")
    last_name = input("Efternamn: ")
    birth_date = input("Födelsedatum (ÅÅÅÅ-MM-DD): ")
    
    birth_year = int(birth_date.split("-")[0])
    current_year = 2026
    age = current_year - birth_year
    
    clean_date = birth_date.replace("-", "")[2:]
    p_number = f"{clean_date}-1234"
    
    cursor.execute('''
        INSERT INTO Users (first_name, last_name, birth_date, p_number, age)
        VALUES (?, ?, ?, ?, ?)
    ''', (first_name, last_name, birth_date, p_number, age))
    conn.commit()
    
    print(f"Användare registrerad! Ålder: {age}, Personnummer: {p_number}")
    return cursor.lastrowid

