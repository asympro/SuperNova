import os
import sys
import rfq_processor
import trade_processor

from functools import reduce
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

def convert(lst):
    # using reduce function to cumulatively apply lambda function to each element
    # in the list and concatenate them with space
    return reduce(lambda x,y: x + ' ' + y, lst)


def rfq(update: Update, context: CallbackContext) -> None:
    """Process the RFQ"""
    user = update.message.from_user
    message = rfq_processor.process_request(convert(context.args), user)
    update.message.reply_text(message)

def trade(update: Update, context: CallbackContext) -> None:
    """Process the RFQ"""
    user = update.message.from_user
    args = ' '.join(context.args)
    args = args.lower()
    if args != 'mine' or args != 'yours':
        update.message.reply_text('type "mine" to buy or "yours" to sell')
    else:
        last_rfq = rfq_processor.get_last_rfq(user)
        message = trade_processor.process_request(context.args, last_rfq)
        update.message.reply_text(message)

def main() -> None:
    """Start the bot."""
    # Fetch the token from environment variable
    TOKEN = os.getenv('SUPERNOVA_BOT_KEY')
    global updater
    updater = Updater(TOKEN, use_context=True)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("kill", kill))
    dispatcher.add_handler(CommandHandler("rfq", rfq))
    dispatcher.add_handler(CommandHandler("trade", trade))

    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
