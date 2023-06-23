import sqlite3
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from better_profanity import profanity


TOKEN = '*************************************'

# Initialize the profanity filter
profanity.load_censor_words()

# Connect to the SQLite database
conn = sqlite3.connect('chat_history.db')
cursor = conn.cursor()

# Create a table to store chat history if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS chat_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        message TEXT
    )
''')
conn.commit()

# Define a function to handle the /start command
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hello! I'm your Telegram bot. How can I assist you?")

# Define a function to handle incoming messages
def echo(update, context):
    message = update.message.text.lower()
    user_id = update.effective_chat.id

    if message.startswith('/'):
        # Handle commands
        command = message[1:]
        handle_command(update, context, command)
    else:
        # Handle general messages
        handle_message(update, context, message, user_id)

def handle_command(update, context, command):
    if command == 'help':
        context.bot.send_message(chat_id=update.effective_chat.id, text="You requested help. How can I assist you?")
    elif command == 'greet':
        context.bot.send_message(chat_id=update.effective_chat.id, text="Hello! How are you?")
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I don't recognize that command. Type /help for assistance.")

def handle_message(update, context, message, user_id):
    # Check for vulgar language
    if has_vulgar_language(message):
        context.bot.send_message(chat_id=update.effective_chat.id, text="Your message contains vulgar language. Please refrain from using offensive words.")
    else:
        # Save the message to the database
        save_message(user_id, message)
        
        # Retrieve previous messages from the database
        chat_history = get_chat_history(user_id)

        # Echo the received message
        context.bot.send_message(chat_id=update.effective_chat.id, text="You said: " + message)

        # Display previous messages
        context.bot.send_message(chat_id=update.effective_chat.id, text="Chat History:")
        for history in chat_history:
            context.bot.send_message(chat_id=update.effective_chat.id, text=history)

        # Check for triggers or keywords and send automated reply
        if 'weather' in message:
            send_weather_update(update, context)
        elif 'joke' in message:
            send_joke(update, context)
        # Add more trigger-based responses as needed

def has_vulgar_language(text):
    # Use better-profanity library to detect vulgar language
    return profanity.contains_profanity(text)

def save_message(user_id, message):
    # Save the message to the database
    cursor.execute('''
        INSERT INTO chat_history (user_id, message) VALUES (?, ?)
    ''', (user_id, message))
    conn.commit()

def get_chat_history(user_id):
    # Retrieve chat history for the user
    cursor.execute('''
        SELECT message FROM chat_history WHERE user_id = ? ORDER BY id DESC LIMIT 5
    ''', (user_id,))
    rows = cursor.fetchall()
    chat_history = [row[0] for row in rows]
    return chat_history[::-1]

def send_weather_update(update, context):
    # Logic to fetch weather information from an API and send an update
    # You can replace this with your own weather API integration
    weather_info = "Today's weather is sunny"
    context.bot.send_message(chat_id=update.effective_chat.id, text=weather_info)

def send_joke(update, context):
    # Logic to fetch a random joke and send it as a response
    # You can replace this with your own joke retrieval mechanism
    joke = "Why don't scientists trust atoms?\nBecause they make up everything!"
    context.bot.send_message(chat_id=update.effective_chat.id, text=joke)

def main():
    # Create the Updater and pass in your bot's API token
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Register the /start command handler
    dispatcher.add_handler(CommandHandler('start', start))

    # Register the echo message handler
    dispatcher.add_handler(MessageHandler(Filters.text, echo))

    # Start the bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C
    updater.idle()

if __name__ == '__main__':
    main()
