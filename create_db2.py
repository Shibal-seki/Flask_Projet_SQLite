
import sqlite3

# Connexion à la base de données SQLite
connection = sqlite3.connect('library.db')

# Lecture et exécution du fichier de schéma SQL
with open('schema2.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

# Insertion des données dans la table Books
cur.execute("INSERT INTO Books (Title, Author, Genre, PublishedYear, Stock) VALUES (?, ?, ?, ?, ?)",
            ('Le Petit Prince', 'Antoine de Saint-Exupéry', 'Fiction', 1943, 10))
cur.execute("INSERT INTO Books (Title, Author, Genre, PublishedYear, Stock) VALUES (?, ?, ?, ?, ?)",
            ('1984', 'George Orwell', 'Dystopia', 1949, 5))
cur.execute("INSERT INTO Books (Title, Author, Genre, PublishedYear, Stock) VALUES (?, ?, ?, ?, ?)",
            ('To Kill a Mockingbird', 'Harper Lee', 'Fiction', 1960, 8))
cur.execute("INSERT INTO Books (Title, Author, Genre, PublishedYear, Stock) VALUES (?, ?, ?, ?, ?)",
            ('Pride and Prejudice', 'Jane Austen', 'Romance', 1813, 7))
cur.execute("INSERT INTO Books (Title, Author, Genre, PublishedYear, Stock) VALUES (?, ?, ?, ?, ?)",
            ('The Great Gatsby', 'F. Scott Fitzgerald', 'Fiction', 1925, 6))

# Insertion des données dans la table Users
cur.execute("INSERT INTO Users (FirstName, LastName, Email, PasswordHash) VALUES (?, ?, ?, ?)",
            ('Emilie', 'Dupont', 'emilie.dupont@example.com', 'hashed_password_1'))
cur.execute("INSERT INTO Users (FirstName, LastName, Email, PasswordHash) VALUES (?, ?, ?, ?)",
            ('Lucas', 'Leroux', 'lucas.leroux@example.com', 'hashed_password_2'))
cur.execute("INSERT INTO Users (FirstName, LastName, Email, PasswordHash) VALUES (?, ?, ?, ?)",
            ('Amandine', 'Martin', 'amandine.martin@example.com', 'hashed_password_3'))
cur.execute("INSERT INTO Users (FirstName, LastName, Email, PasswordHash) VALUES (?, ?, ?, ?)",
            ('Antoine', 'Tremblay', 'antoine.tremblay@example.com', 'hashed_password_4'))
cur.execute("INSERT INTO Users (FirstName, LastName, Email, PasswordHash) VALUES (?, ?, ?, ?)",
            ('Sarah', 'Lambert', 'sarah.lambert@example.com', 'hashed_password_5'))

# Insertion des données dans la table BorrowedBooks
cur.execute("INSERT INTO BorrowedBooks (UserID, BookID, BorrowDate) VALUES (?, ?, ?)",
            (1, 2, '2023-01-15'))
cur.execute("INSERT INTO BorrowedBooks (UserID, BookID, BorrowDate) VALUES (?, ?, ?)",
            (2, 1, '2023-01-20'))
cur.execute("INSERT INTO BorrowedBooks (UserID, BookID, BorrowDate) VALUES (?, ?, ?)",
            (3, 4, '2023-01-25'))

# Insertion des données dans la table Transactions
cur.execute("INSERT INTO Transactions (BookID, TransactionType, Quantity) VALUES (?, ?, ?)",
            (1, 'Addition', 10))
cur.execute("INSERT INTO Transactions (BookID, TransactionType, Quantity) VALUES (?, ?, ?)",
            (2, 'Addition', 5))
cur.execute("INSERT INTO Transactions (BookID, TransactionType, Quantity) VALUES (?, ?, ?)",
            (3, 'Addition', 8))
cur.execute("INSERT INTO Transactions (BookID, TransactionType, Quantity) VALUES (?, ?, ?)",
            (4, 'Addition', 7))
cur.execute("INSERT INTO Transactions (BookID, TransactionType, Quantity) VALUES (?, ?, ?)",
            (5, 'Addition', 6))

# Validation des changements
connection.commit()

# Fermeture de la connexion
connection.close()
