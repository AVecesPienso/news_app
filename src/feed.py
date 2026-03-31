from datetime import datetime

def print_feed(news_list, game_name):
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