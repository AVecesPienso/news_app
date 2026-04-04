import os
from dotenv import load_dotenv
from src import igdb_client, menu

def main(token, client_id):
    """
    Entry point of the application.
    Initializes the CLI menu with the provided IGDB credentials.
    """
    menu.show_menu(token, client_id)
    
if __name__ == "__main__":
    load_dotenv()
    client_id = os.getenv("TWITCH_CLIENT_ID")
    client_secret = os.getenv("TWITCH_CLIENT_SECRET")
    token = igdb_client.get_token(client_id, client_secret)
    main(token, client_id)