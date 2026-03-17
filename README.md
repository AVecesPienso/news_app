# IGDB News App

This is an app designed to fetch video game news connected to the **IGDB API** through **Twitch OAuth2**.

## Current features:
- Secure environment setup (`.env`).
- Automated authentication with the Twitch API to obtain an `Access Token`.
- Isolated dependency management using a virtual environment (`venv`).

## Requirements:
- **Python 3.12** or higher.
- A [Twitch Developers](https://dev.twitch.tv/) account to obtain API credentials.

## Instalation and Setup:

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
    pip install requests python-dotenv
    ```
4. **Configure your credentials:**
    - Create a file named `.env` in the root directory
    - Copy the following text and replace it with your data
    ```
    TWITCH_CLIENT_ID=your_client_id_here
    TWITCH_CLIENT_SECRET=your_client_secret_here
    ```
## Usage:
```
python main.py
```