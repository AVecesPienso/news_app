from src import igdb_client, news_client, feed, bookmarks

def show_menu(token, client_id):
    while True:
        print("1. View Popular games feed")
        print("2. Search a game")
        print("3. View and edit bookmarks")
        print("0. Exit")
        choice = input("\nSelect an option: ")


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
                    save = input("\nSave as bookmark? (Y/N): ")
                    if save.lower() == "y":
                        if bookmarks.save_bookmark(result["name"], steam_ids, result["franchise_id"], result["collection_id"]):
                            print("Bookmark saved!")
                else:
                    print("No news found for this game.")
            else:
                print("Game not found.")

        elif choice == "3":
            content = bookmarks.load_bookmark()
            if not content:
                print("No bookmarks saved yet.")
            else:
                for i, bookmark in enumerate(content):
                    print(f"{i + 1}. {bookmark['name']}")
                print("0. Back")
                selected = None
                while True:
                    try:
                        selection = int(input("\nSelect a bookmark to edit: "))
                        if selection == 0:
                            break
                        if selection < 0 or selection > len(content):
                            print("Invalid option.")
                        else:
                            selected = content[selection - 1]
                            break
                    except ValueError:
                        print("Please enter a valid number.")
                if selected:
                    while True:
                        print("1. View news")
                        print("2. Delete bookmark")
                        print("0. Back")
                        selection = input("\nSelect an option: ")

                        if selection == "1":
                            news = news_client.get_news(selected["steam_ids"])
                            if news:
                                feed.print_feed(news, selected["name"])
                                break
                            else:
                                print("No news found for this bookmark.")
                        elif selection == "2":
                            bookmarks.delete_bookmark(selected["name"])
                            print("Bookmark Deleted.")
                            break
                        elif selection == "0":
                            break

        elif choice == "0":
            break

        else:
            print("Invalid option.")