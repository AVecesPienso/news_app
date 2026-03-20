import os
import requests
from dotenv import load_dotenv

load_dotenv()
client_id = os.getenv("TWITCH_CLIENT_ID")
client_secret = os.getenv("TWITCH_CLIENT_SECRET")

def get_token(c_id, c_secret):
    request_data = {
        "client_id" : c_id, 
        "client_secret" : c_secret, 
        "grant_type" : "client_credentials"
        }
    twitch_url = "https://id.twitch.tv/oauth2/token"
    
    response = requests.post(twitch_url, request_data)
    response.raise_for_status()
    token = response.json().get("access_token")
    return token

def query_igdb(endpoint, body, token, client_id):
    url = f"https://api.igdb.com/v4/{endpoint}"
    headers = {
        "Client-ID": client_id,
        "Authorization": f"Bearer {token}"
    }
    response = requests.post(url, headers=headers, data=body)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"IGDB Error [{response.status_code}] at {endpoint}")
        return None

def get_game_data(game_name, token, client_id):
    body = f'search "{game_name}"; fields id, name, summary, franchises; limit 10;'
    return query_igdb("games", body, token, client_id)
    
def get_franchise_data(franchise_id, token, client_id):
    body = f'fields name, games; where id = {franchise_id};'
    return query_igdb("franchises", body, token, client_id)

def main():
    token = get_token(client_id, client_secret)
    game = input("Enter game to search: ")
    games_list = get_game_data(game, token, client_id)

    if games_list:
        print(f"\n{len(games_list)} games found:")

        for game in games_list:
            name = game.get('name', 'N/A')
            summary = game.get('summary', 'N/A')
            game_id = game.get('id', 'N/A')

            print(f"\nName: [{game_id}] {name}")
            print(summary)
            print("-" * 30)

    selected_game = games_list[0]
    franchise_ids = selected_game.get('franchises', [])
    
    if franchise_ids:
        f_id = franchise_ids[0]
        franchise_data = get_franchise_data(f_id, token, client_id)

        if franchise_data:
            data = franchise_data[0]
            print(f"\n--- Franchise feed: {data['name']} ---")
            print(f"Linked games: {data['games']}")
    else:
        print("\nThis game doesn't belong to a franchise, printing individual news")
    
if __name__ == "__main__":
    main()