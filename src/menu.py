import os
import sys
from src import igdb_client, news_client, feed, bookmarks
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.prompt import Prompt
from src.shared import console

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def show_menu(token, client_id):
    """
    Displays the main CLI menu and handles user navigation.
    Options: view popular feed, search a game, manage bookmarks, and exit.
    """
    while True:
        clear_screen()
        console.print(Panel("[yellow]IGDB News App[/yellow]", style="bold cyan on #101B21"))

        menu_table = Text.assemble(
            ("1. ", "bold cyan"), ("View Popular games feed", "bold white"), "\n",
            ("2. ", "bold cyan"), ("Search a game", "bold white"), "\n",
            ("3. ", "bold cyan"), ("View and edit bookmarks", "bold white"), "\n",
            "\n",
            ("0. Exit", "bold red")
        )
        console.print(Panel(menu_table, title="[bold purple]Main Menu[/bold purple]", title_align="left", style="bold cyan on #101B21"))

        choice = Prompt.ask("\n[bold cyan]>[/bold cyan] [bold white]Select an option[/bold white]")

        if choice == "1":
            clear_screen()
            with console.status("[bold green]Searching IGDB..."):
                feed.popular_feed(token, client_id)
            while True:
                option_menu = Text.assemble(
                    ("0. Back", "bold red")
                )
                console.print(Panel(option_menu, style="bold cyan on #101B21"))
                action = Prompt.ask("\n[bold cyan]>[/bold cyan] [bold white]Select an option[/bold white]", default="0", show_default=False)

                if action == "0":
                    clear_screen()
                    break
                else:
                    console.print("[bold red]Please enter a valid number.[/bold red]")
                    Prompt.ask("[dim]Press Enter[/dim]")
                    for _ in range(7): 
                        sys.stdout.write("\x1b[1A\x1b[2K") 
                    sys.stdout.flush()

        elif choice == "2":
            while True:
                clear_screen()
                header_text = Text.assemble(
                    "Type a game name to fetch its latest news.\n",
                    ("Or press ", "dim"), 
                    ("0 ", "bold red"),
                    ("or ", "dim"),
                    ("Enter", "bold red"),
                    (" to go back to Main Menu.", "dim")
                    )
                console.print(Panel(header_text, title="[bold purple]Game News Finder[/bold purple]", title_align="left", style="bold cyan on #101B21"))

                game_name = Prompt.ask("\n[bold cyan]>[/bold cyan] [bold white]Game Name[/bold white]", default="0", show_default=False)
                if game_name == "0":
                    clear_screen()
                    break

                with console.status("[bold green]Searching IGDB..."):
                    result = igdb_client.process_request(game_name, token, client_id)

                if result:
                    steam_ids = [item["uid"] for item in result["steam_ids"]][:10]
                    with console.status("[bold blue]Fetching Steam News..."):
                        news = news_client.get_news(steam_ids)

                    if news:
                        clear_screen()
                        feed.print_feed(news, result["name"])

                        while True:
                            options_menu = Text.assemble(
                                ("1. ", "bold cyan"), ("Save as bookmark", "bold white"), "\n",
                                ("0. Back", "bold red")
                            )
                            console.print(Panel(options_menu, style="bold cyan on #101B21"))
                            action = Prompt.ask("\n[bold cyan]>[/bold cyan] [bold white]Select an option[/bold white]", default="0", show_default=False)
                            if action == "0":
                                clear_screen()
                                break
                            elif action == "1":
                                clear_screen()
                                bookmarks.save_bookmark(result["name"], steam_ids, result["franchise_id"], result["collection_id"])
                                Prompt.ask("[dim]Press Enter to continue[/dim]")
                                clear_screen()
                                break
                            else:
                                console.print("[bold red]Please enter a valid number.[/bold red]")
                                Prompt.ask("[dim]Press Enter[/dim]")
                                for _ in range(8): 
                                    sys.stdout.write("\x1b[1A\x1b[2K") 
                                sys.stdout.flush()
                    else:
                        console.print("[yellow]⚠ No news found for this game.[/yellow]")
                        Prompt.ask("[dim]Press Enter[/dim]")
                else:
                    console.print("[red]✖ Game not found.[/red]")
                    Prompt.ask("[dim]Press Enter[/dim]")

        elif choice == "3":
            while True:
                clear_screen()
                content = bookmarks.load_bookmark()
                if not content:
                    console.print(Panel("No bookmarks saved yet.", style="yellow"))
                    Prompt.ask("[dim]Press Enter to continue[/dim]")
                    clear_screen()
                    break
                else:
                    table = Table.grid(padding=(0, 1))
                    for i, bookmark in enumerate(content):
                        table.add_row(f"[bold cyan]{i + 1}.[/bold cyan]", f"[bold white]{bookmark['name']}[/bold white]")
                    table.add_row("", "")
                    table.add_row("[bold red]0.[/bold red]", "[bold red]Back[/bold red]")
                    console.print(Panel(table, title="[yellow]Bookmarks[/yellow]", title_align="left", style="bold cyan on #101B21"))

                    selection = Prompt.ask("\n[bold cyan]>[/bold cyan] [bold white]Select a bookmark to edit[/bold white]", default="0", show_default=False)
                    if selection == "0":
                        clear_screen()
                        break
                    try:
                        index = int(selection) - 1
                        if 0 <= index < len(content):
                            selected = content[index]

                            while True:
                                clear_screen()
                                action_table = Text.assemble(
                                    ("1. ", "bold cyan"), ("View news", "bold white"), "\n",
                                    ("2. ", "bold cyan"), ("Delete bookmark", "bold white"), "\n",
                                    "\n",
                                    ("0. Back", "bold red")
                                )
                                console.print(Panel(action_table, title=f"[yellow]{selected['name']}[/yellow]", title_align="left", style="bold cyan on #101B21"))
                                action = Prompt.ask("\n[bold cyan]>[/bold cyan] [bold white]Select an option[/bold white]", default="0", show_default=False)

                                if action == "1":
                                    with console.status(f"[bold blue]Loading news for {selected['name']}..."):
                                        news = news_client.get_news(selected["steam_ids"])
                                    if news:
                                        clear_screen()
                                        feed.print_feed(news, selected["name"])
                                        Prompt.ask("\n[dim]Press Enter to go back[/dim]")
                                    else:
                                        console.print("[yellow]No news found.[/yellow]")
                                        Prompt.ask("[dim]Press Enter[/dim]")

                                elif action == "2":
                                    clear_screen()
                                    bookmarks.delete_bookmark(selected["name"])
                                    console.print("[bold red]✖ Bookmark deleted.[/bold red]")
                                    Prompt.ask("[dim]Press Enter[/dim]")
                                    break

                                elif action == "0":
                                    clear_screen()
                                    break

                                else:
                                    console.print("[bold red]Please enter a valid number.[/bold red]")
                                    Prompt.ask("[dim]Press Enter[/dim]")
                        else:
                            console.print("[bold red]Please enter a valid number.[/bold red]")
                            Prompt.ask("[dim]Press Enter[/dim]")
                    except ValueError:
                        console.print("[bold red]Please enter a valid number.[/bold red]")
                        Prompt.ask("[dim]Press Enter[/dim]")

        elif choice == "0":
            clear_screen()
            break

        else:
            console.print("[bold red]Please enter a valid number.[/bold red]")
            Prompt.ask("[dim]Press Enter[/dim]")