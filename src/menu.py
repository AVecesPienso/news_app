from src import igdb_client, news_client, feed

def show_menu(token, client_id):
    while True:
        print("1. View Popular games feed")
        print("2. Search a game")
        print("3. View bookmarks")
        print("4. Exit")
        choice = input("\nSelect an option:")

        if choice == "1":
            feed.popular_feed(token, client_id)
        elif choice == "2":
            game_name = input("\nEnter game name: ")
            result = igdb_client.process_request(game_name, token, client_id)
            if result:
                steam_ids = [item["uid"] for item in result["steam_ids"]][:10]
                news = news_client.get_news(steam_ids)
                if news:
                    feed.print_feed(news, result["name"])
                else:
                    print("No news found for this game.")
            else:
                print("Game not found.")
        elif choice == "3":
            print("Coming soon...")
        elif choice == "4":
            break
        else:
            print("Invalid option")