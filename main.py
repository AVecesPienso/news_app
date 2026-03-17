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