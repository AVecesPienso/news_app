from src import igdb_client, news_client
from datetime import datetime, timedelta
from rich.panel import Panel
from rich.console import Group
from rich.text import Text
from src.shared import console

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
    panels = []
    for item in news_list:
        feedlabel = item["feedlabel"]
        date = datetime.fromtimestamp(item["date"]).strftime("%B %d, %Y")
        title = item["title"]
        author = item["author"] if item["author"] else "Unknown"
        url = item["url"]

        news_text = Text.assemble(
            (f"[{feedlabel}]", "bold magenta"), " ",(title, "bold white"), "\n",
            ("Date: ", "bold cyan"), (date, "bold white"), "\n",
            ("Author: ", "bold cyan"), (author, "bold white"), "\n",
            ("URL: ", "bold cyan"), (url, "underline blue")
        )
        panels.append(Panel(news_text, style="bold cyan on #101B21"))

    group = Panel(Group(*panels), title=f"[yellow]{game_name}", title_align="left", border_style="bold purple")
    console.print(group)
    console.print("\n")
    