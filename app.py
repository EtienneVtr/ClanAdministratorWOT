from flask import Flask, render_template, redirect, request, session, url_for
import os
from dotenv import load_dotenv

from src.utils import *

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

app = Flask(__name__)

# Charger la clé secrète depuis les variables d'environnement
app.secret_key = os.getenv('FLASK_SECRET_KEY')

# L'ID de l'application fourni par Wargaming
APPLICATION_ID = "c7571fd57ca5f64661bb378bf38bb08c"
REDIRECT_URI = "http://127.0.0.1:5000/callback"  # URL où l'utilisateur est redirigé après connexion

# Dictionnaire pour suivre les réserves activées
activated_reserves = {}

# Désactive les logs pour les requêtes vers l'API Wargaming
@app.before_request
def silence_logs():
    if request.endpoint in ['callback']:
        import logging
        logging.getLogger('werkzeug').setLevel(logging.ERROR)

@app.context_processor
def inject_player():
    # Vérifie si un utilisateur est connecté
    nickname = session.get('nickname')
    clan_name = session.get('clan_name')
    role = get_position(APPLICATION_ID, session.get('account_id')) if clan_name != "Aucun clan" and clan_name else ""
    player = {
        "nickname": nickname,
        "clan_name": clan_name,
        "role": role,
        "can_use_reserve": can_use_reserve(role)
    }
    return {'player': player, 'emblem': session.get('emblem')}

@app.route('/')
def index():
    return render_template('index.html')

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
    session['clan_name'] = get_clan_name(APPLICATION_ID, account_id)
    session['emblem'] = get_clan_emblem(APPLICATION_ID, session.get('clan_name')) if session.get('clan_name') != "Aucun clan" or not session.get('clan_name') else None
    
    if session.get('emblem') :
        save_path = os.path.join(app.root_path, 'static\\img\\emblem.jpg')
        if download_image(session.get('emblem'), save_path):
            print("Image téléchargée avec succès.")
        else:
            print("Erreur lors du téléchargement de l'image.")

    # Redirection vers la page principale
    return redirect(url_for('index'))

@app.route('/reserves', methods=['GET', 'POST'])
def reserves():
    global activated_reserves
    
    if request.method == 'GET':
        access_token = session.get('access_token')
        reserves = get_reserves(APPLICATION_ID, access_token)
        
        # Vérifie si une réserve est activée
        for reserve in reserves: 
            for stock in reserve['in_stock']:
                if stock['active_till'] is not None:
                    activated_reserves[reserve['name']] = True
        
        # Ajoute un attribut à reserve.stock pour savoir si on peut activer la réserve
        for reserve in reserves:
            for stock in reserve['in_stock']:
                stock['activable'] = is_activable(reserve['name'], activated_reserves)
        
        return render_template('reserves.html', reserves=reserves)
    else:
        # Activation d'une réserve
        reserve_name = request.form.get('name')
        reserve_type = request.form.get('type')
        reserve_level = request.form.get('level')
        
        if is_activable(reserve_name, activated_reserves):
            activated_reserves[reserve_name] = True
            # Activation de la réserve !! À FAIRE SEULEMENT AVEC XORION !!
            # url = f"https://api.worldoftanks.eu/wot/stronghold/activateclanreserve/?application_id={APPLICATION_ID}&access_token={session.get('access_token')}&reserve_level={reserve_level}&reserve_type={reserve_type}"
            # response = requests.post(url)
            return redirect(url_for('reserves'))
        
        return redirect(url_for('reserves'))

@app.route('/logout')
def logout():
    # Supprime toutes les données de session
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
