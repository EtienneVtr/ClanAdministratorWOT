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