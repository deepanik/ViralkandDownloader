# Telegram Bot - ViralkandDownloader

A simple Telegram bot that responds to commands.

## Setup

1. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

2. Activate the virtual environment:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On Linux/Mac:
     ```bash
     source venv/bin/activate
     ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Get your bot token from [@BotFather](https://t.me/BotFather) on Telegram

5. Update `config.py` with your bot token:
   ```python
   BOT_TOKEN = "your_actual_bot_token_here"
   ```

6. Run the bot:
   ```bash
   python main.py
   ```

## Commands

- `/start` - Bot responds with "Hello"
- `/rand` - Bot responds with "Im active darling"

