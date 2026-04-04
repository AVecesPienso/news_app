import os
from src import igdb_client, news_client, feed, bookmarks

def show_menu(token, client_id):
    """
    Displays the main CLI menu and handles user navigation.
    Options: view popular feed, search a game, manage bookmarks, and exit.
    """
    os.system('clear')
    while True:
        print("1. View Popular games feed")
        print("2. Search a game")
        print("3. View and edit bookmarks")
        print("0. Exit")
        choice = input("\nSelect an option: ")
        os.system('clear')

        if choice == "1":
            feed.popular_feed(token, client_id)
            while True:
                print("0. Back")
                action = input("\nSelect an option: ")
                if action == "0":
                    os.system('clear')
                    break
                else:
                    print("Invalid option.")

        elif choice == "2":
            while True:
                game_name = input("\nEnter game name: \n0. Cancel\n> ")
                if game_name == "0":
                    os.system('clear')
                    break
                os.system('clear')
                result = igdb_client.process_request(game_name, token, client_id)
                if result:
                    steam_ids = [item["uid"] for item in result["steam_ids"]][:10]
                    news = news_client.get_news(steam_ids)
                    if news:
                        feed.print_feed(news, result["name"])
                        while True:
                            print("\n1. Save as bookmark")
                            print("0. Back")
                            save = input("\nSelect an option: ")
                            if save == "0":
                                os.system('clear')
                                break
                            elif save == "1":
                                os.system('clear')
                                bookmarks.save_bookmark(result["name"], steam_ids, result["franchise_id"], result["collection_id"])
                                input("\nPress Enter to continue...")
                                os.system('clear')
                                break
                            else:
                                print("Invalid option.")
                    else:
                        print("No news found for this game.")
                else:
                    print("Game not found.")

        elif choice == "3":
            while True:
                content = bookmarks.load_bookmark()
                if not content:
                    print("No bookmarks saved yet.")
                    input("\nPress Enter to continue...")
                    os.system('clear')
                    break
                else:
                    for i, bookmark in enumerate(content):
                        print(f"{i + 1}. {bookmark['name']}")
                    print("0. Back")
                    selected = None
                    go_back = False
                    while True:
                        try:
                            selection = int(input("\nSelect a bookmark to edit: "))
                            os.system('clear')
                            if selection == 0:
                                go_back = True
                                break
                            if selection < 0 or selection > len(content):
                                print("Invalid option.")
                            else:
                                selected = content[selection - 1]
                                break
                        except ValueError:
                            print("Please enter a valid number.")
                    if go_back:
                        break
                    if selected:
                        while True:
                            print("1. View news")
                            print("2. Delete bookmark")
                            print("0. Back")
                            selection = input("\nSelect an option: ")
                            os.system('clear')
                            if selection == "1":
                                news = news_client.get_news(selected["steam_ids"])
                                if news:
                                    feed.print_feed(news, selected["name"])
                                    while True:
                                        print("\n0. Back")
                                        action = input("\nSelect an option: ")
                                        if action == "0":
                                            os.system('clear')
                                            break
                                        else:
                                            print("Invalid option.")
                                    break
                                else:
                                    print("No news found for this bookmark.")
                            elif selection == "2":
                                bookmarks.delete_bookmark(selected["name"])
                                print("Bookmark Deleted.")
                                input("\nPress Enter to continue...")
                                os.system('clear')
                                break
                            elif selection == "0":
                                break

        elif choice == "0":
            break

        else:
            print("Invalid option.")