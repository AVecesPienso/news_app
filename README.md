# IGDB News App

This is an app designed to fetch video game news connected to the **IGDB API** through **Twitch OAuth2**.

## How it works:
The app follows a 3-step data expansion flow:
1. **Search:** Translates user input into a specific `Game ID`.
2. **Expand:** Pivots from the `Game ID` to its `Franchise ID`.
3. **Map:** Retrieves the full list of all `Linked Game IDs` within that franchise to prepare for the news feed.

## Current features:
- **Modular API Wrapper:** A unified `query_igdb` engine for efficient endpoint communication.
- **Relational Data Mapping:** Automatically identifies a game's franchise and expands search to all related titles.
- **Franchise News Aggregator (In Progress):** Logic to group game IDs for bulk news fetching.
- **Secure Environment:** Full `.env` integration and automated Twitch OAuth2 handshake.

## Requirements:
- **Python 3.12** or higher.
- **Libraries:** `requests` (API communication) and `python-dotenv` (credential management).
- A [Twitch Developers](https://dev.twitch.tv/) account for API credentials.

## Installation and Setup:

1. **Clone the repository:**
   ```
   git clone https://github.com/AVecesPienso/news_app.git
   cd news_app
   ```
2. **Create and activate virtual environment:**
    ```
    python3 -m venv venv
    source venv/bin/activate
    ```
3. **Install dependencies:**
    ```
    pip install -r requirements.txt
    ```
4. **Configure your credentials:**
    - Create a file named `.env` in the root directory
    - Copy the following text and replace it with your data

    ```
    TWITCH_CLIENT_ID=your_client_id_here
    TWITCH_CLIENT_SECRET=your_client_secret_here
    ```
## Usage:
Run the main script and enter a game title when prompted:
```
python main.py
```
### Example output:
```
-Enter game to search: The Witcher 3

8 games found:

Name: [1942] The Witcher 3: Wild Hunt
The Witcher 3: Wild Hunt is an open-world action role-playing game developed by CD Projekt Red.

Set in a dark fantasy world, the game follows Geralt of Rivia, a monster hunter searching for his adopted daughter, Ciri, while navigating political conflicts and supernatural threats. Gameplay features exploration, combat, character progression, and branching narratives shaped by player choices. Widely acclaimed for its writing, world-building, and depth, it is considered one of the most influential RPGs of its generation.
------------------------------

--- Franchise feed: The Witcher ---
Linked games: [80, 478, 1942, 9689, 12503, 19474, 27832, 8765, 107300, 122661, 115776, 137125, 119402, 194662, 187249, 198179, 208307, 220276, 220277, 230102, 16209, 23473, 22319, 13166, 170451, 170450, 226413, 157580, 170449, 141472, 20740, 387351, 314927, 20275, 22439, 44549, 372654]
```

## Roadmap:
- [ ] Convert Game IDs to Steam AppIDs via `external_games`.
- [ ] Fetch live patch notes and announcements using the Steam News API.
- [ ] Implement a clean CLI or Web interface for news display.