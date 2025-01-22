-- Table pour les utilisateurs
CREATE TABLE Utilisateurs (
    id_utilisateur INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    mot_de_passe VARCHAR(255) NOT NULL,
    role ENUM('Utilisateur', 'Administrateur') DEFAULT 'Utilisateur', -- Contrôle d'accès
    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table pour les livres
CREATE TABLE Livres (
    id_livre INT AUTO_INCREMENT PRIMARY KEY,
    titre VARCHAR(200) NOT NULL,
    auteur VARCHAR(150) NOT NULL,
    categorie VARCHAR(100),
    isbn VARCHAR(20) UNIQUE NOT NULL,
    quantite_totale INT DEFAULT 1, -- Gestion des stocks
    quantite_disponible INT DEFAULT 1,
    date_publication DATE,
    date_ajout TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table pour les emprunts
CREATE TABLE Emprunts (
    id_emprunt INT AUTO_INCREMENT PRIMARY KEY,
    id_utilisateur INT NOT NULL,
    id_livre INT NOT NULL,
    date_emprunt DATE NOT NULL,
    date_retour DATE,
    statut ENUM('En cours', 'Terminé') DEFAULT 'En cours',
    FOREIGN KEY (id_utilisateur) REFERENCES Utilisateurs(id_utilisateur) ON DELETE CASCADE,
    FOREIGN KEY (id_livre) REFERENCES Livres(id_livre) ON DELETE CASCADE
);

-- Table pour les recommandations (optionnelle)
CREATE TABLE Recommendations (
    id_recommendation INT AUTO_INCREMENT PRIMARY KEY,
    id_utilisateur INT NOT NULL,
    id_livre INT NOT NULL,
    score INT CHECK (score BETWEEN 1 AND 5),
    commentaire TEXT,
    FOREIGN KEY (id_utilisateur) REFERENCES Utilisateurs(id_utilisateur) ON DELETE CASCADE,
    FOREIGN KEY (id_livre) REFERENCES Livres(id_livre) ON DELETE CASCADE
);

-- Table pour les notifications (optionnelle)
CREATE TABLE Notifications (
    id_notification INT AUTO_INCREMENT PRIMARY KEY,
    id_utilisateur INT NOT NULL,
    message TEXT NOT NULL,
    date_notification TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    statut ENUM('Non lu', 'Lu') DEFAULT 'Non lu',
    FOREIGN KEY (id_utilisateur) REFERENCES Utilisateurs(id_utilisateur) ON DELETE CASCADE
);

-- Table pour les rapports statistiques (optionnelle)
CREATE TABLE Statistiques (
    id_statistique INT AUTO_INCREMENT PRIMARY KEY,
    id_livre INT NOT NULL,
    emprunts_totaux INT DEFAULT 0,
    dernier_emprunt DATE,
    FOREIGN KEY (id_livre) REFERENCES Livres(id_livre) ON DELETE CASCADE
);
