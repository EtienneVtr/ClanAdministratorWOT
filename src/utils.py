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