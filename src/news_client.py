import requests

def get_news(id_list):
    url = "https://api.steampowered.com/ISteamNews/GetNewsForApp/v2/"
    news = []
    for steam_id in id_list:
        try:
            params = {
                "appid" : steam_id,
                "count" : 5,
                "format" : "json"
            }
            response = requests.get(url, params=params)
            data = response.json()
            news_items = data["appnews"]["newsitems"]
            news_items = [n for n in news_items if not n.get("feedname", "").endswith(".ru")]
            news.extend(news_items)
        except KeyError:
            pass
        except Exception as e:
            print(f"Error with Steam ID {steam_id}: {e}")
    return news