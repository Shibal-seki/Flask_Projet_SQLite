-- Table des utilisateurs
CREATE TABLE Utilisateurs (
    id INTEGER PRIMARY KEY AUTOINCREMENT, -- Identifiant unique
    prenom TEXT NOT NULL,                 -- Prénom de l'utilisateur
    nom TEXT NOT NULL,                    -- Nom de l'utilisateur
    email TEXT NOT NULL UNIQUE            -- Adresse email unique
);

-- Table des commandes
CREATE TABLE Commandes (
    id INTEGER PRIMARY KEY AUTOINCREMENT, -- Identifiant unique de la commande
    utilisateur_id INTEGER NOT NULL,      -- Clé étrangère vers l'utilisateur
    date_commande TEXT NOT NULL,          -- Date de la commande (format ISO 8601)
    montant REAL NOT NULL,                -- Montant total de la commande
    statut TEXT DEFAULT 'En attente',     -- Statut de la commande (ex: En attente, Livrée)
    FOREIGN KEY (utilisateur_id) REFERENCES Utilisateurs(id) -- Relation avec Utilisateurs
);
