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

def loan_book(user_id):
    cursor.execute("SELECT id, title, author FROM Books")
    books = cursor.fetchall()
    print("\nTILLGÄNGLIGA BÖCKER:")
    for b in books:
        print(f"[{b[0]}] {b[1]} av {b[2]}")
        
    book_id = int(input("Ange ID på boken du vill låna: "))
    
    cursor.execute("INSERT INTO Loans (user_id, book_id) VALUES (?, ?)", (user_id, book_id))
    conn.commit()
    print("Boken har nu lånats!")

def show_user_page(user_id):
    print("\n--- DIN SIDA (Lånade böcker) ---")
    cursor.execute('''
        SELECT Books.title, Books.author FROM Loans
        JOIN Books ON Loans.book_id = Books.id
        WHERE Loans.user_id = ?
    ''', (user_id,))
    loans = cursor.fetchall()
    if not loans:
        print("Du har inte lånat några böcker än.")
    for l in loans:
        print(f"- {l[0]} ({l[1]})")

def show_admin_page():
    print("\n--- BIBLIOTEKETS SIDA (Alla utlånade böcker) ---")
    cursor.execute('''
        SELECT Books.title, Users.first_name, Users.last_name FROM Loans
        JOIN Books ON Loans.book_id = Books.id
        JOIN Users ON Loans.user_id = Users.id
    ''')
    all_loans = cursor.fetchall()
    if not all_loans:
        print("Inga böcker är utlånade just nu.")
    for al in all_loans:
        print(f"Bok: '{al[0]}' är lånad av: {al[1]} {al[2]}")

def main():
    print("Välkommen till Biblioteket!")
    user_id = register_user()
    
    while True:
        print("\nMENY:")
        print("1. Låna en bok")
        print("2. Visa Mina Lån (Användarens lånade böcker)")
        print("3. Visa Alla Lån (Bibliotekets alla utlånade böcker)")
        print("4. Avsluta")
        
        val = input("Välj (1-4): ")
        if val == "1":
            loan_book(user_id)
        elif val == "2":
            show_user_page(user_id)
        elif val == "3":
            show_admin_page()
        elif val == "4":
            break

    conn.close()

if __name__ == '__main__':
    main()


