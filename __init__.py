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

# Fonction d'initialisation de la base de données
def init_db():
    connection = sqlite3.connect('clients.db')
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            prenom TEXT NOT NULL,
            adresse TEXT NOT NULL
        )
    ''')
    # Insérer des données si elles n'existent pas
    cursor.execute('SELECT COUNT(*) FROM clients')
    if cursor.fetchone()[0] == 0:
        cursor.executemany('''
            INSERT INTO clients (nom, prenom, adresse)
            VALUES (?, ?, ?)
        ''', [
            ('DUPONT', 'Emilie', '123, Rue des Lilas, 75001 Paris'),
            ('LEROUX', 'Lucas', '456, Avenue du Soleil, 31000 Toulouse'),
            ('MARTIN', 'Amandine', '789, Rue des Érables, 69002 Lyon'),
            ('TREMBLAY', 'Antoine', '1010, Boulevard de la Mer, 13008 Marseille'),
            ('LAMBERT', 'Sarah', '222, Avenue de la Liberté, 59000 Lille'),
            ('GAGNON', 'Nicolas', '456, Boulevard des Cerisiers, 69003 Lyon'),
            ('DUBOIS', 'Charlotte', '789, Rue des Roses, 13005 Marseille'),
            ('LEFEVRE', 'Thomas', '333, Rue de la Paix, 75002 Paris')
        ])
    connection.commit()
    connection.close()

# Route principale avec la barre de recherche
@app.route('/')
def index():
    return '''
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Recherche Client</title>
    </head>
    <body>
        <h1>Rechercher un Client</h1>
        <form action="/search" method="GET">
            <input type="text" name="query" placeholder="Entrez un nom ou un prénom" required>
            <button type="submit">Rechercher</button>
        </form>
    </body>
    </html>
    '''

# Route pour effectuer la recherche
@app.route('/fiche_nom/', methods=['GET'])
def search():
    query = request.args.get('query', '').strip()  # Terme recherché
    if not query:
        return jsonify({"error": "Veuillez entrer un terme à rechercher"}), 400

    connection = sqlite3.connect('clients.db')
    cursor = connection.cursor()
    
    # Rechercher dans les colonnes 'nom' et 'prenom'
    cursor.execute('''
        SELECT * FROM clients
        WHERE nom LIKE ? OR prenom LIKE ?
    ''', (f'%{query}%', f'%{query}%'))
    results = cursor.fetchall()
    connection.close()

    # Construire les résultats
    if results:
        return jsonify([{"id": row[0], "nom": row[1], "prenom": row[2], "adresse": row[3]} for row in results])
    else:
        return jsonify({"message": f"Aucun client trouvé pour le terme '{query}'"}), 404


#test
                                                                                                                                       
if __name__ == "__main__":
  app.run(debug=True)
