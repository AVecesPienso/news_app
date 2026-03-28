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
- **Franchise News Aggregator:** Logic to group game IDs for bulk news fetching.
- **Steam News Integration:** Fetches live news articles for all games in a franchise via the Steam News API
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

## Project Structure:
```
news_app/
├── main.py
├── requirements.txt
├── .env
├── .gitignore
├── src/
│   ├── igdb_client.py
│   ├── news_client.py
│   └── feed.py
└── data/
    └── bookmarks.json  ← generated automatically on first run
```

## Usage:
Run the main script and enter a game title when prompted:
```
python main.py
```
### Example output:
```
Enter game to search: The Witcher

47 news articles found for: The Witcher

[PC Gamer] The Witcher 3 modders are still discovering and restoring deleted scenes...
Author: Robin Valentine
URL: https://www.pcgamer.com/...
```

## Roadmap:
- [x] Convert Game IDs to Steam AppIDs via `external_games`.
- [x] Fetch live patch notes and announcements using the Steam News API.
- [ ] Format news feed for readable CLI display (feed.py).
- [ ] Implement bookmarks system with JSON storage.
- [ ] Build interactive CLI menu.