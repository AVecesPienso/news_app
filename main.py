import os
from dotenv import load_dotenv
from src import igdb_client, news_client, feed

def main(token, client_id):
    game_name = input("Enter game to search: ")
    result = igdb_client.process_request(game_name, token, client_id)
    steam_ids = [item["uid"] for item in result["steam_ids"]]
    
    news_list = news_client.get_news(steam_ids)
    print(f"{len(news_list)} news found")
    feed.print_feed(news_list)
    
if __name__ == "__main__":
    load_dotenv()
    client_id = os.getenv("TWITCH_CLIENT_ID")
    client_secret = os.getenv("TWITCH_CLIENT_SECRET")
    token = igdb_client.get_token(client_id, client_secret)
    main(token, client_id)