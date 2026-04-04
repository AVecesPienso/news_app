import requests
from datetime import datetime, timedelta

def get_token(client_id, client_secret):
    """
    Requests an OAuth2 access token from Twitch.
    Returns the access token as a string.
    """
    twitch_url = "https://id.twitch.tv/oauth2/token"
    request_data = {
        "client_id" : client_id, 
        "client_secret" : client_secret, 
        "grant_type" : "client_credentials"
        }

    response = requests.post(twitch_url, request_data)
    response.raise_for_status()
    token = response.json().get("access_token")
    return token

def query_igdb(endpoint, body, token, client_id):
    """
    API query wrapper.
    Sends a POST request to the IGDB API and returns the JSON response.
    Returns None if the request fails.
    """
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
    """
    Uses query_igdb wrapper.
    Requests game name, id, franchises and collection by searching user input game name.
    Limited at 10 results
    """
    body = f'fields id, name, franchises, collection; search "{game_name}"; limit 10;'
    return query_igdb("games", body, token, client_id)
    
def get_franchise_data(franchise_id, token, client_id):
    """
    Uses query_igdb wrapper.
    Requests franchise name and related games by IDs.
    """
    body = f'fields name, games; where id = {franchise_id};'
    return query_igdb("franchises", body, token, client_id)

def get_collection_data(collection_id, token, client_id):
    """
    Uses query_igdb wrapper.
    Requests collection name and related games by IDs.
    """
    body = f'fields name, games; where id = {collection_id};'
    return query_igdb("collections", body, token, client_id)

def get_popular_games(token, client_id):
    """
    Uses query_igdb wrapper.
    Requests the most popular games in the last 2 years.
    Determined by total_rating_count and hypes, limited to a total of 20 games.
    """
    years_ago = datetime.now() - timedelta(days=365*2)
    timestamp = int(years_ago.timestamp())
    body = f'fields id, name, franchises, collection, total_rating_count, hypes; where (total_rating_count > 100 | hypes > 50) & first_release_date > {timestamp}; sort total_rating_count desc; limit 20;'
    return query_igdb("games", body, token, client_id)

def get_steam_data(game_ids, token, client_id):
    """
    Uses query_igdb wrapper.
    Fetches Steam App IDs for a list of IGDB game IDs via the external_games endpoint.
    Filters out non-Steam entries and duplicate IDs.
    Returns a list of dicts with 'game' (IGDB ID) and 'uid' (Steam App ID).
    """
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

def resolve_steam_ids(game_dict, token, client_id):
    """
    Resolves Steam App IDs for a game by expanding its franchise or collection.
    If the game has no franchise or collection, uses its own IGDB ID as fallback.
    Returns a list of dicts with 'game' (IGDB ID) and 'uid' (Steam App ID).
    """
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

    return get_steam_data(target_ids, token, client_id)

def process_feed(game_dict, token, client_id):
    """
    Processes a game from the popular feed and resolves its Steam App IDs.
    Receives a game dict from get_popular_games.
    Returns a dict with 'name' and 'steam_ids'.
    """
    steam_data = resolve_steam_ids(game_dict, token, client_id)
    return {"name": game_dict['name'], "steam_ids": steam_data}

def process_request(game_name, token, client_id):
    """
    Searches IGDB for a game by name and resolves its Steam App IDs.
    Prioritizes exact name matches, falls back to the first result.
    Returns a dict with 'name', 'steam_ids', 'franchise_id', and 'collection_id'.
    Returns None if no results are found. 
    """
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

    franchises = selected_game.get('franchises')
    collection_id = selected_game.get('collection')
    steam_data = resolve_steam_ids(selected_game, token, client_id)
    return {"name": selected_game['name'], 
            "steam_ids": steam_data, 
            "franchise_id": franchises[0] if franchises else None,
            "collection_id": collection_id if collection_id else None
            }