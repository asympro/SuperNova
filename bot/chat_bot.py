import os
import sys
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')

def echo(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    update.message.reply_text(update.message.text)

def kill(update: Update, context: CallbackContext) -> None:
    """Stop the bot and exit the process when the command /kill is issued."""
    update.message.reply_text('Shutting down...')
    updater.stop()
    sys.exit(0)

def main() -> None:
    """Start the bot."""
    # Fetch the token from environment variable
    TOKEN = os.getenv('SUPERNOVA_BOT_KEY')
    global updater
    updater = Updater(TOKEN, use_context=True)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("kill", kill))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()