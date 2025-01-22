from flask import Flask, render_template_string, render_template, jsonify, request, redirect, url_for, session
from flask import render_template
from flask import json
from urllib.request import urlopen
from werkzeug.utils import secure_filename
import sqlite3

app = Flask(__name__)                                                                                                                   
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'  # Clé secrète pour les sessions

# Fonction pour créer une clé "authentifie" dans la session utilisateur
def est_authentifie():
    return session.get('authentifie')

@app.route('/')
def hello_world():
    return render_template('hello.html')

@app.route('/lecture')
def lecture():
    if not est_authentifie():
        # Rediriger vers la page d'authentification si l'utilisateur n'est pas authentifié
        return redirect(url_for('authentification'))

  # Si l'utilisateur est authentifié
    return "<h2>Bravo, vous êtes authentifié</h2>"



@app.route('/authentification', methods=['GET', 'POST'])
def authentification():
    if request.method == 'POST':
        # Vérifier les identifiants
        if request.form['username'] == 'admin' and request.form['password'] == 'password': # password à cacher par la suite
            session['authentifie'] = True
            # Rediriger vers la route lecture après une authentification réussie
            return redirect(url_for('lecture'))
        else:
            # Afficher un message d'erreur si les identifiants sont incorrects
            return render_template('formulaire_authentification.html', error=True)

    return render_template('formulaire_authentification.html', error=False)

@app.route('/fiche_client/<int:post_id>')
def Readfiche(post_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM clients WHERE id = ?', (post_id,))
    data = cursor.fetchall()
    conn.close()
    # Rendre le template HTML et transmettre les données
    return render_template('read_data.html', data=data)

@app.route('/consultation/')
def ReadBDD():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM clients;')
    data = cursor.fetchall()
    conn.close()
    return render_template('read_data.html', data=data)

@app.route('/enregistrer_client', methods=['GET'])
def formulaire_client():
    return render_template('formulaire.html')  # afficher le formulaire

@app.route('/enregistrer_client', methods=['POST'])
def enregistrer_client():
    nom = request.form['nom']
    prenom = request.form['prenom']

    # Connexion à la base de données
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Exécution de la requête SQL pour insérer un nouveau client
    cursor.execute('INSERT INTO clients (created, nom, prenom, adresse) VALUES (?, ?, ?, ?)', (1002938, nom, prenom, "ICI"))
    conn.commit()
    conn.close()
    return redirect('/consultation/')  # Rediriger vers la page d'accueil après l'enregistrement




# Route pour afficher et mettre à jour un utilisateur
@app.route('/update_user_library/<int:user_id>/', methods=['GET', 'POST'])
def update_user(user_id):
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()

    # Récupérer les informations de l'utilisateur actuel
    cursor.execute("SELECT UserID, FirstName, LastName, Email FROM Users WHERE UserID = ?", (user_id,))
    user = cursor.fetchone()

    if not user:
        flash('Utilisateur non trouvé', 'danger')
        return redirect('/user_library/')

    if request.method == 'POST':
        # Récupérer les données du formulaire
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']

        # Si le mot de passe est renseigné, on le hash
        password_hash = generate_password_hash(password) if password else user[4]  # Si aucun mot de passe, on garde l'existant

        # Mettre à jour les informations dans la base de données
        try:
            cursor.execute("""
                UPDATE Users 
                SET FirstName = ?, LastName = ?, Email = ?, PasswordHash = ? 
                WHERE UserID = ?
            """, (first_name, last_name, email, password_hash, user_id))
            conn.commit()
            flash('Utilisateur mis à jour avec succès', 'success')
            return redirect('/users_library/')  # Rediriger vers la page des utilisateurs
        except sqlite3.IntegrityError:
            flash('Erreur : Email déjà utilisé.', 'danger')

    conn.close()

    # Si la méthode est GET, afficher le formulaire pré-rempli avec les données existantes
    return render_template('update_user.html', user=user)

# Route pour afficher la liste des utilisateurs
@app.route('/users_library/')
def users_library():
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    cursor.execute("SELECT UserID, FirstName, LastName, Email, DateCreated FROM Users;")
    data = cursor.fetchall()
    conn.close()
    return render_template('user_library.html', data=data)
                                                                                                                                       
if __name__ == "__main__":
  app.run(debug=True)


