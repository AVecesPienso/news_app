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

def get_game_list(game_name, token, client_id):
    game_request_path = "https://api.igdb.com/v4/games"
    headers = {
        "Client-ID": client_id,
        "Authorization": f"Bearer {token}"
    }
    body = f'search "{game_name}"; fields id, name, summary; limit 10;'
    response = requests.post(game_request_path, headers=headers, data=body)

    if response.status_code == 200:
        response_data = response.json()
        if response_data:
            return response_data
    else:
        print(f"Search error: {response.status_code}")
        return None
    
def main():
   token = get_token(client_id, client_secret)
   game = input("Enter game to search: ")
   games_list = get_game_list(game, token, client_id)

   if games_list:
       print(f"\n{len(games_list)} games found:")

       for game in games_list:
        name = game.get('name', 'N/A')
        summary = game.get('summary', 'N/A')
        game_id = game.get('id', 'N/A')

        print(f"\nName: [{game_id}] {name}")
        print(summary)
    
if __name__ == "__main__":
    main()