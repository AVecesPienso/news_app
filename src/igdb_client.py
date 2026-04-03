import requests
from datetime import datetime, timedelta

def get_token(c_id, c_secret):
    twitch_url = "https://id.twitch.tv/oauth2/token"
    request_data = {
        "client_id" : c_id, 
        "client_secret" : c_secret, 
        "grant_type" : "client_credentials"
        }

    response = requests.post(twitch_url, request_data)
    response.raise_for_status()
    token = response.json().get("access_token")
    return token

def query_igdb(endpoint, body, token, client_id):
    url = f"https://api.igdb.com/v4/{endpoint}"
    headers = {
        "Client-ID": client_id,
        "Authorization": f"Bearer {token}",
        "Content-Type": "text/plain"
    }
    response = requests.post(url, headers=headers, data=body)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"IGDB Error [{response.status_code}] at {endpoint}")
        return None

def get_game_data(game_name, token, client_id):
    body = f'fields id, name, franchises, collection; search "{game_name}"; limit 10;'
    return query_igdb("games", body, token, client_id)
    
def get_franchise_data(franchise_id, token, client_id):
    body = f'fields name, games; where id = {franchise_id};'
    return query_igdb("franchises", body, token, client_id)

def get_collection_data(collection_id, token, client_id):
    body = f'fields name, games; where id = {collection_id};'
    return query_igdb("collections", body, token, client_id)

def get_popular_games(token, client_id):
    years_ago = datetime.now() - timedelta(days=365*2)
    timestamp = int(years_ago.timestamp())
    body = f'fields id, name, franchises, collection, total_rating_count, hypes; where (total_rating_count > 100 | hypes > 50) & first_release_date > {timestamp}; sort total_rating_count desc; limit 20;'
    return query_igdb("games", body, token, client_id)

def get_steam_data(game_ids, token, client_id):
    if not game_ids:
        return [] 
    
    ids_string = ",".join(map(str, game_ids))
    body = f"fields game, uid, category; where game = ({ids_string}); limit 500;"
    results = query_igdb("external_games", body, token, client_id)

    if not results:
        return []

    steam_data = []
    seen = set()

    for item in results:
        uid = item.get("uid")
        game_id = item.get("game")
        category = item.get("category")

        if category == 1 or (not category and uid and uid.isdigit()):
            identifier = f"{game_id}-{uid}"
            
            if identifier not in seen:
                steam_data.append({
                    "game": game_id,
                    "uid": uid
                })
                seen.add(identifier)
    
    return steam_data

def process_request(game_name, token, client_id):
    game_results = get_game_data(game_name, token, client_id)
    if not game_results:
        return None
    
    selected_game = None
    for g in game_results:
        if g['name'].lower() == game_name.lower():
            selected_game = g
            break
    if selected_game is None:
        selected_game = game_results[0]

    name = selected_game['name']
    franchises = selected_game.get('franchises')
    collection_id = selected_game.get('collection')
    target_ids = []

    if franchises:
        f_results = get_franchise_data(franchises[0], token, client_id)
        target_ids = f_results[0].get('games', []) if f_results else []
    elif collection_id:
        c_results = get_collection_data(collection_id, token, client_id)
        target_ids = c_results[0].get('games', []) if c_results else []
    else:
        target_ids = [selected_game['id']]

    steam_data = get_steam_data(target_ids, token, client_id)
    return {"name": name, 
            "steam_ids": steam_data, 
            "franchise_id": franchises[0] if franchises else None,
            "collection_id": collection_id if collection_id else None
            }

def process_feed(game_dict, token, client_id):
    name = game_dict['name']
    franchises = game_dict.get('franchises')
    collection_id = game_dict.get('collection')
    target_ids = []

    if franchises:
        f_results = get_franchise_data(franchises[0], token, client_id)
        target_ids = f_results[0].get('games', []) if f_results else []
    elif collection_id:
        c_results = get_collection_data(collection_id, token, client_id)
        target_ids = c_results[0].get('games', []) if c_results else []
    else:
        target_ids = [game_dict['id']]

    steam_data = get_steam_data(target_ids, token, client_id)
    return {"name": name, "steam_ids": steam_data}