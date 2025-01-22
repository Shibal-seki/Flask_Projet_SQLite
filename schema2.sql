DROP TABLE IF EXISTS Books;
CREATE TABLE Books (
    BookID INTEGER PRIMARY KEY, -- Gère automatiquement l'auto-incrémentation
    Title TEXT NOT NULL,
    Author TEXT NOT NULL,
    Genre TEXT,
    PublishedYear INTEGER,
    Stock INTEGER NOT NULL DEFAULT 0
);

DROP TABLE IF EXISTS Users;
CREATE TABLE Users (
    UserID INTEGER PRIMARY KEY, -- Gère automatiquement l'auto-incrémentation
    FirstName TEXT NOT NULL,
    LastName TEXT NOT NULL,
    Email TEXT UNIQUE NOT NULL,
    PasswordHash TEXT NOT NULL,
    DateCreated DATETIME DEFAULT CURRENT_TIMESTAMP
);

DROP TABLE IF EXISTS BorrowedBooks;
CREATE TABLE BorrowedBooks (
    BorrowID INTEGER PRIMARY KEY, -- Gère automatiquement l'auto-incrémentation
    UserID INTEGER NOT NULL,
    BookID INTEGER NOT NULL,
    BorrowDate DATE NOT NULL DEFAULT CURRENT_DATE,
    ReturnDate DATE,
    FOREIGN KEY (UserID) REFERENCES Users(UserID),
    FOREIGN KEY (BookID) REFERENCES Books(BookID)
);

DROP TABLE IF EXISTS Transactions;
CREATE TABLE Transactions (
    TransactionID INTEGER PRIMARY KEY, -- Gère automatiquement l'auto-incrémentation
    BookID INTEGER NOT NULL,
    TransactionType TEXT NOT NULL,
    Quantity INTEGER NOT NULL,
    TransactionDate DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (BookID) REFERENCES Books(BookID)
);
