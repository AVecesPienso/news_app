from src import igdb_client, news_client
from datetime import datetime, timedelta

def popular_feed(token, client_id):
    """
    Fetches popular games from IGDB and displays their news in the terminal.
    Prioritizes news from the game itself over franchise-related titles.
    Filters out articles older than 2 years.
    """
    popular = igdb_client.get_popular_games(token, client_id)
    years_ago = datetime.now() - timedelta(days=365*2)
    timestamp = int(years_ago.timestamp())
    for game_dict in popular:
        result = igdb_client.process_feed(game_dict, token, client_id)
        if result:
            main_ids = [item["uid"] for item in result["steam_ids"] if item["game"] == game_dict["id"]]
            franchise_ids = [item["uid"] for item in result["steam_ids"] if item["game"] != game_dict["id"]]
            steam_ids = (main_ids + franchise_ids)[:10]
            news = news_client.get_news(steam_ids)
            news = [n for n in news if n["date"] > timestamp]
            if news:
                print_feed(news, game_dict['name'])

def print_feed(news_list, game_name):
    """
    Formats and prints a list of news articles to the terminal.
    Displays game name as header followed by each article's source, date, title, author and URL.
    """
    print("-" * 30)
    print(game_name)
    print("-" * 30)
    for item in news_list:
        feedlabel = item["feedlabel"]
        date = datetime.fromtimestamp(item["date"]).strftime("%B %d, %Y")
        title = item["title"]
        author = item["author"] if item["author"] else "Unknown"
        url = item["url"]
    
        print(f"[{feedlabel}] {date}")
        print(title)
        print(f"Author: {author}")
        print(f"URL: {url}")
        print("-" * 30)