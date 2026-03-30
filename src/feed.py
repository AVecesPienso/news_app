from datetime import datetime

def print_feed(news_list):
    for item in news_list:
        feedlabel = item["feedlabel"]
        date = datetime.fromtimestamp(item["date"]).strftime("%B %d, %Y")
        title = item["title"]
        author = item["author"] if item["author"] else "Unknown"
        url = item["url"]
    
        print("-" * 30)
        print(f"[{feedlabel}] {date}")
        print(title)
        print(f"Author: {author}")
        print(f"URL: {url}")
        print("-" * 30)