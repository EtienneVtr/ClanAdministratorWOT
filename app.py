from flask import Flask, render_template, redirect, request, session, url_for
import os
from dotenv import load_dotenv
import requests

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

app = Flask(__name__)

# Charger la clé secrète depuis les variables d'environnement
app.secret_key = os.getenv('FLASK_SECRET_KEY')

# L'ID de l'application fourni par Wargaming
APPLICATION_ID = "c7571fd57ca5f64661bb378bf38bb08c"
REDIRECT_URI = "http://127.0.0.1:5000/callback"  # URL où l'utilisateur est redirigé après connexion

@app.route('/')
def index():
    # Vérifie si un utilisateur est connecté
    nickname = session.get('nickname')  # Récupération du pseudo depuis la session
    clan_name = session.get('clan_name')  # Récupération du nom du clan depuis la session
    return render_template('index.html', nickname=nickname, clan_name=clan_name)

@app.route('/login')
def login():
    # URL de l'API Wargaming pour la connexion
    auth_url = f"https://api.worldoftanks.eu/wot/auth/login/?application_id={APPLICATION_ID}&redirect_uri={REDIRECT_URI}"
    return redirect(auth_url)

@app.route('/callback')
def callback():
    # Récupération des données envoyées par Wargaming
    status = request.args.get('status')
    access_token = request.args.get('access_token')
    expires_at = request.args.get('expires_at')
    account_id = request.args.get('account_id')
    nickname = request.args.get('nickname')

    # Vérification du statut
    if status != "ok":
        return "Erreur de connexion.", 400

    # Stockage des informations utilisateur dans la session
    session['access_token'] = access_token
    session['expires_at'] = expires_at
    session['account_id'] = account_id
    session['nickname'] = nickname
    
    # Récupération du nom du clan
    url = f"https://api.worldoftanks.eu/wot/clans/memberhistory/?application_id={APPLICATION_ID}&account_id={account_id}&language=en"
    response = requests.get(url)
    data = response.json()
    if data["data"][account_id] == []:
        clan_name = "Aucun clan"
    else:
        clan_id = data["data"].get(str(account_id), [])[0].get("clan_id", None)
        url = f"https://api.worldoftanks.eu/wot/clans/info/?application_id={APPLICATION_ID}&clan_id={clan_id}"
        response = requests.get(url)
        data = response.json()
        clan_name = data["data"].get(str(clan_id), {}).get("tag", None)
    session['clan_name'] = clan_name

    # Redirection vers la page principale
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    # Supprime toutes les données de session
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
