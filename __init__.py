from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'  # Clé secrète pour les sessions

# Dictionnaire des utilisateurs pour l'authentification
utilisateurs = {
    "admin": {"password": "admin123", "role": "Admin"},
    "user": {"password": "12345", "role": "User"}
}

# Fonction pour vérifier si un utilisateur est authentifié
def est_authentifie():
    return session.get('authentifie', False)

# Fonction pour vérifier si l'utilisateur est admin
def est_admin():
    return session.get('role') == 'Admin'

# Route principale redirigeant vers les pages spécifiques en fonction du rôle
@app.route('/')
def index():
    if not est_authentifie():  # Vérifier si l'utilisateur est authentifié
        return redirect(url_for('authentification'))

    if est_admin():
        return redirect(url_for('admin_home'))
    else:
        return redirect(url_for('user_home'))

# Route pour l'authentification
@app.route('/authentification', methods=['GET', 'POST'])
def authentification():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username in utilisateurs and utilisateurs[username]["password"] == password:
            session['authentifie'] = True
            session['role'] = utilisateurs[username]["role"]
            session['utilisateur_id'] = username
            return redirect(url_for('index'))

        return render_template('formulaire_authentification.html', error=True)

    return render_template('formulaire_authentification.html', error=False)

# Route pour se déconnecter
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('authentification'))

# Route pour la page Admin
@app.route('/admin_home', methods=['GET', 'POST'])
def admin_home():
    if not est_authentifie() or not est_admin():
        return "<h2>Accès refusé : Vous devez être administrateur pour accéder à cette page.</h2>", 403

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    if request.method == 'POST':
        if 'ajouter_livre' in request.form:
            titre = request.form['titre']
            auteur = request.form['auteur']
            annee = request.form['annee']
            quantite = request.form['quantite']
            cursor.execute('INSERT INTO Livres (Titre, Auteur, Annee_publication, Quantite) VALUES (?, ?, ?, ?)', 
                           (titre, auteur, annee, quantite))
            conn.commit()

        if 'supprimer_livre' in request.form:
            livre_id = request.form['livre_id']
            cursor.execute('DELETE FROM Livres WHERE ID_livre = ?', (livre_id,))
            conn.commit()

        if 'ajouter_stock' in request.form:
            livre_id = request.form['livre_id']
            quantite_ajoutee = request.form['quantite']
            cursor.execute('UPDATE Livres SET Quantite = Quantite + ? WHERE ID_livre = ?', (quantite_ajoutee, livre_id))
            conn.commit()

    cursor.execute('SELECT * FROM Livres')
    livres = cursor.fetchall()
    conn.close()

    return render_template('admin_home.html', livres=livres)

@app.route('/user_home', methods=['GET', 'POST'])
def user_home():
    if not est_authentifie() or est_admin():
        return "<h2>Accès refusé : Vous devez être utilisateur pour accéder à cette page.</h2>", 403

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    if request.method == 'POST':
        if 'emprunter' in request.form:
            livre_id = request.form['livre_id']
            cursor.execute('SELECT Quantite FROM Livres WHERE ID_livre = ?', (livre_id,))
            livre = cursor.fetchone()
            if livre and livre[0] > 0:
                cursor.execute('UPDATE Livres SET Quantite = Quantite - 1 WHERE ID_livre = ?', (livre_id,))
                cursor.execute('INSERT INTO Emprunts (ID_utilisateur, ID_livre) VALUES (?, ?)', 
                               (session['utilisateur_id'], livre_id))
                conn.commit()

        if 'retourner' in request.form:
            emprunt_id = request.form['emprunt_id']
            cursor.execute('SELECT ID_livre FROM Emprunts WHERE ID_emprunt = ?', (emprunt_id,))
            emprunt = cursor.fetchone()
            if emprunt:
                cursor.execute('UPDATE Livres SET Quantite = Quantite + 1 WHERE ID_livre = ?', (emprunt[0],))
                cursor.execute('UPDATE Emprunts SET Statut = "Terminé", Date_retour = DATE("now") WHERE ID_emprunt = ?', 
                               (emprunt_id,))
                conn.commit()

    cursor.execute('SELECT * FROM Livres')
    livres = cursor.fetchall()

    cursor.execute('''
        SELECT E.ID_emprunt, L.Titre, L.Auteur, E.Date_emprunt, E.Statut
        FROM Emprunts E
        JOIN Livres L ON E.ID_livre = L.ID_livre
        WHERE E.ID_utilisateur = ? AND E.Statut = "Actif"
    ''', (session['utilisateur_id'],))
    emprunts = cursor.fetchall()

    conn.close()

    return render_template('user_home.html', livres=livres, emprunts=emprunts)

if __name__ == "__main__":
    app.run(debug=True)
