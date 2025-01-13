import requests

def get_clan_name(application_id, account_id):
    # Récupération du nom du clan
    url = f"https://api.worldoftanks.eu/wot/account/info/?application_id={application_id}&account_id={account_id}"
    response = requests.get(url)
    data = response.json()
    clan_id = data["data"][account_id]["clan_id"]
    if clan_id == None:
        clan_name = "Aucun clan"
    else:
        url = f"https://api.worldoftanks.eu/wot/clans/info/?application_id={application_id}&clan_id={clan_id}"
        response = requests.get(url)
        data = response.json()
        clan_name = data["data"].get(str(clan_id), {}).get("tag", None)
    return clan_name

def get_position(application_id, account_id):
    # Récupération du rôle dans le clan
    url = f"https://api.worldoftanks.eu/wot/clans/accountinfo/?application_id={application_id}&account_id={account_id}&language=fr&fields=role_i18n"
    response = requests.get(url)
    data = response.json()
    role = data["data"][account_id]["role_i18n"]
    return role

def can_use_reserve(role):
    # Vérifie si le joueur peut utiliser les réserves
    if role in ["Commandant", "Commandant en second", "Officier du personnel", "Officier de combat"]:
        return True
    else :
        return False
    
def get_reserves(application_id, access_token):
    # Récupération des réserves
    url = f"https://api.worldoftanks.eu/wot/stronghold/clanreserves/?application_id={application_id}&access_token={access_token}&language=fr&fields=bonus_type%2C+disposable%2C+name%2C+type%2C+in_stock.amount%2C+in_stock.level%2C+in_stock.action_time%2C+in_stock.active_till%2C+in_stock.bonus_values"
    response = requests.get(url)
    data = response.json()
    
    '''
    {'status': 'ok', 'meta': {'count': 7}, 'data': [{'type': 'ADDITIONAL_BRIEFING', 'in_stock': [{'amount': 7, 'active_till': None, 'bonus_values': [{'value': 4.0, 'battle_type': 'Batailles de clan et Tournois'}, {'value': 3.0, 'battle_type': 'Batailles aléatoires'}], 'level': 12}], 'disposable': False, 'name': 'Briefing supplémentaire', 'bonus_type': "à l'EXP. d'équipage obtenue"}, {'type': 'ARTILLERY_STRIKE', 'in_stock': [{'amount': 102, 'active_till': None, 'bonus_values': [{'value': 0.28, 'battle_type': 'Escarmouches et Batailles de Bastion'}], 'level': 9}, {'amount': 7, 'active_till': None, 'bonus_values': [{'value': 1.0, 'battle_type': 'Escarmouches et Batailles de Bastion'}], 'level': 12}], 'disposable': True, 'name': "Frappe d'artillerie", 'bonus_type': 'aux Ressources industrielles obtenues'}, {'type': 'BATTLE_PAYMENTS', 'in_stock': [{'amount': 13, 'active_till': None, 'bonus_values': [{'value': 0.5, 'battle_type': 'Batailles de clan et Tournois'}, {'value': 0.25, 'battle_type': 'Batailles aléatoires'}], 'level': 9}, {'amount': 2, 'active_till': None, 'bonus_values': [{'value': 1.5, 'battle_type': 'Batailles de clan et Tournois'}, {'value': 0.3, 'battle_type': 'Batailles aléatoires'}], 'level': 12}], 'disposable': False, 'name': 'Paiements des batailles', 'bonus_type': 'aux crédits obtenus'}, {'type': 'HIGH_CAPACITY_TRANSPORT', 'in_stock': [{'amount': 14, 'active_till': None, 'bonus_values': [{'value': 0.6, 'battle_type': 'Escarmouches et Batailles de Bastion'}], 'level': 10}], 'disposable': True, 'name': 'Transport de grande capacité', 'bonus_type': 'aux Ressources industrielles obtenues'}, {'type': 'INSPIRATION', 'in_stock': [{'amount': 106, 'active_till': None, 'bonus_values': [{'value': 0.28, 'battle_type': 'Escarmouches et Batailles de Bastion'}], 'level': 9}, {'amount': 2, 'active_till': None, 'bonus_values': [{'value': 0.5, 'battle_type': 'Escarmouches et Batailles de Bastion'}], 'level': 11}, {'amount': 5, 'active_till': None, 'bonus_values': [{'value': 1.0, 'battle_type': 'Escarmouches et Batailles de Bastion'}], 'level': 12}], 'disposable': True, 'name': 'Inspiration', 'bonus_type': 'aux Ressources industrielles obtenues'}, {'type': 'REQUISITION', 'in_stock': [{'amount': 2, 'active_till': None, 'bonus_values': [{'value': 0.55, 'battle_type': 'Batailles de Bastion'}], 'level': 9}], 'disposable': True, 'name': 'Réquisition', 'bonus_type': 'aux Ressources industrielles obtenues'}, {'type': 'TACTICAL_TRAINING', 'in_stock': [{'amount': 13, 'active_till': None, 'bonus_values': [{'value': 1.0, 'battle_type': 'Toutes les batailles'}], 'level': 12}], 'disposable': False, 'name': 'Entraînement tactique', 'bonus_type': "à l'EXP. de bataille obtenue"}]}
    '''
    '''# Ajout factice de la date d'expiration pour tester l'activation des réserves
    for reserve in data["data"]:
        if reserve["name"] == "Briefing supplémentaire":
            reserve["in_stock"][0]["active_till"] = "2021-09-30T00:00:00"'''
    
    return data["data"]

def is_activable(reserve_name, activated_reserves):
    # Vérifie si une réserve peut être activée en fonction des réserves déjà activées
    incompatible_reserves = {
        "Manoeuvres militaires": "Briefing supplémentaire",
        "Paiements des batailles": "Entraînement tactique"
    }
    
    # Si le nombre de réserves activées est déjà 2, on ne peut pas en ajouter
    if len(activated_reserves) == 2:
        return False
    
    # Si aucune réserve n'est activée, la réserve peut être activée
    if len(activated_reserves) == 0:
        return True
    
    # Si la réserve est déjà activée, on ne peut pas la réactiver
    if activated_reserves.get(reserve_name, False):
        return False
    
    # Vérifie si la réserve est incompatible avec une autre déjà activée
    for activated_reserve in activated_reserves:
        if reserve_name == incompatible_reserves.get(activated_reserve, None):
            return False
    
    # Si aucune condition d'incompatibilité n'est rencontrée, la réserve peut être activée
    return True

def get_clan_id(application_id, clan_name):
    # Récupération de l'ID du clan
    url = f"https://api.worldoftanks.eu/wot/clans/list/?application_id={application_id}&search={clan_name}"
    response = requests.get(url)
    data = response.json()
    clan_id = data["data"][0]["clan_id"]
    return clan_id

def get_clan_emblem(application_id, clan_name):
    url = f"https://api.worldoftanks.eu/wot/clans/info/?application_id={application_id}&fields=emblems.x195&clan_id={get_clan_id(application_id, clan_name)}"
    response = requests.get(url)
    data = response.json()
    emblem = data["data"][str(get_clan_id(application_id, clan_name))]["emblems"]["x195"]["portal"]
    return emblem

def download_image(image_url, save_path):
    response = requests.get(image_url)
    if response.status_code == 200:
        with open(save_path, 'wb') as file:
            file.write(response.content)
        return True
    return False