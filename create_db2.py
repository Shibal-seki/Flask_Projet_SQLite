import sqlite3

def creer_base_de_donnees(nom_bdd="bibliotheque.db"):
    # Connexion à la base de données (ou création si elle n'existe pas)
    connexion = sqlite3.connect(nom_bdd)
    curseur = connexion.cursor()

    # Création des tables
    # Table Utilisateurs
    curseur.execute("""
    CREATE TABLE IF NOT EXISTS Utilisateurs (
        id_utilisateur INTEGER PRIMARY KEY AUTOINCREMENT,
        nom TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        mot_de_passe TEXT NOT NULL,
        role TEXT CHECK(role IN ('Utilisateur', 'Administrateur')) DEFAULT 'Utilisateur',
        date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # Table Livres
    curseur.execute("""
    CREATE TABLE IF NOT EXISTS Livres (
        id_livre INTEGER PRIMARY KEY AUTOINCREMENT,
        titre TEXT NOT NULL,
        auteur TEXT NOT NULL,
        categorie TEXT,
        isbn TEXT UNIQUE NOT NULL,
        quantite_totale INTEGER DEFAULT 1,
        quantite_disponible INTEGER DEFAULT 1,
        date_publication DATE,
        date_ajout TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # Table Emprunts
    curseur.execute("""
    CREATE TABLE IF NOT EXISTS Emprunts (
        id_emprunt INTEGER PRIMARY KEY AUTOINCREMENT,
        id_utilisateur INTEGER NOT NULL,
        id_livre INTEGER NOT NULL,
        date_emprunt DATE NOT NULL,
        date_retour DATE,
        statut TEXT CHECK(statut IN ('En cours', 'Terminé')) DEFAULT 'En cours',
        FOREIGN KEY (id_utilisateur) REFERENCES Utilisateurs(id_utilisateur) ON DELETE CASCADE,
        FOREIGN KEY (id_livre) REFERENCES Livres(id_livre) ON DELETE CASCADE
    );
    """)

    # Table Recommendations (optionnelle)
    curseur.execute("""
    CREATE TABLE IF NOT EXISTS Recommendations (
        id_recommendation INTEGER PRIMARY KEY AUTOINCREMENT,
        id_utilisateur INTEGER NOT NULL,
        id_livre INTEGER NOT NULL,
        score INTEGER CHECK(score BETWEEN 1 AND 5),
        commentaire TEXT,
        FOREIGN KEY (id_utilisateur) REFERENCES Utilisateurs(id_utilisateur) ON DELETE CASCADE,
        FOREIGN KEY (id_livre) REFERENCES Livres(id_livre) ON DELETE CASCADE
    );
    """)

    # Table Notifications (optionnelle)
    curseur.execute("""
    CREATE TABLE IF NOT EXISTS Notifications (
        id_notification INTEGER PRIMARY KEY AUTOINCREMENT,
        id_utilisateur INTEGER NOT NULL,
        message TEXT NOT NULL,
        date_notification TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        statut TEXT CHECK(statut IN ('Non lu', 'Lu')) DEFAULT 'Non lu',
        FOREIGN KEY (id_utilisateur) REFERENCES Utilisateurs(id_utilisateur) ON DELETE CASCADE
    );
    """)

    # Table Statistiques (optionnelle)
    curseur.execute("""
    CREATE TABLE IF NOT EXISTS Statistiques (
        id_statistique INTEGER PRIMARY KEY AUTOINCREMENT,
        id_livre INTEGER NOT NULL,
        emprunts_totaux INTEGER DEFAULT 0,
        dernier_emprunt DATE,
        FOREIGN KEY (id_livre) REFERENCES Livres(id_livre) ON DELETE CASCADE
    );
    """)

    # Sauvegarde des modifications et fermeture de la connexion
    connexion.commit()
    connexion.close()
    print(f"Base de données '{nom_bdd}' créée avec succès.")

# Appeler la fonction pour créer la base de données
if __name__ == "__main__":
    creer_base_de_donnees()
