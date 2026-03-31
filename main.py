import os
from dotenv import load_dotenv
from src import igdb_client, news_client, feed
from datetime import datetime, timedelta

def main(token, client_id):
    popular = igdb_client.get_popular_games(token, client_id)

    for game_dict in popular:
        result = igdb_client.process_feed(game_dict, token, client_id)
        if result:
            main_ids = [item["uid"] for item in result["steam_ids"] if item["game"] == game_dict["id"]]
            franchise_ids = [item["uid"] for item in result["steam_ids"] if item["game"] != game_dict["id"]]
            steam_ids = (main_ids + franchise_ids)[:10]
            news = news_client.get_news(steam_ids)
            years_ago = datetime.now() - timedelta(days=365*2)
            timestamp = int(years_ago.timestamp())
            news = [n for n in news if n["date"] > timestamp]
            if news:
                feed.print_feed(news, game_dict['name'])
    
if __name__ == "__main__":
    load_dotenv()
    client_id = os.getenv("TWITCH_CLIENT_ID")
    client_secret = os.getenv("TWITCH_CLIENT_SECRET")
    token = igdb_client.get_token(client_id, client_secret)
    main(token, client_id)