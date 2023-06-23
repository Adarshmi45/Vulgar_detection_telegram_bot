# Vulgar_detection_telegram_bot
# Telegram Bot

This is a Telegram bot implemented in Python using the `python-telegram-bot` library. The bot acts as a chat assistant and provides various functionalities.

## Functionality

- `/start` command: Sends a greeting message and starts the conversation with the bot.
- General chat: The bot responds to incoming messages and maintains a chat history.
- Commands:
  - `/help`: Displays a help message to assist the user.
  - `/greet`: Sends a greeting message to the user.
- Automated Replies: The bot detects trigger words and sends automated responses. Currently supported triggers:
  - "weather": Sends a weather update.
  - "joke": Sends a random joke.

## Getting Started

1. Clone the repository:


2. Install the required dependencies:


3. Obtain a Telegram Bot API token from BotFather ([instructions here](https://core.telegram.org/bots#botfather)).

4. Update the `TOKEN` variable in the code (`bot.py`) with your API token.

5. Run the bot:


6. Start chatting with the bot in your Telegram app.


