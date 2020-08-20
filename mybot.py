import logging
import os

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

PORT = int(os.environ.get('PORT', '8443'))
# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.


def start(update, context):
    keyboard = [[InlineKeyboardButton("Start", callback_data='Start'),
                 InlineKeyboardButton("Help", callback_data='help')],
                [InlineKeyboardButton("About", callback_data='Developed by @TympazEngineer')]]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Please choose:', reply_markup=reply_markup)
#Button
def button(update, context):
    query = update.callback_query
    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    query.answer()
    query.edit_message_text(text="Selected option: {}".format(query.data)) 

def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Use /start to start this bot.')


def echo(update, context):
    """Echo the user message."""
    update.message.reply_text(update.message.text)


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    """Start the bot."""

    APP_NAME = os.environ.get('APP_NAME')
    TOKEN = os.environ.get('TOKEN')

    updater = Updater(
        TOKEN, use_context=True)

    dp = updater.dispatcher

    # Handling commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    # Keyboard Button
    dp.add_handler(CallbackQueryHandler(button))
    dp.add_handler(CommandHandler("help", help))

    # If not Command i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_webhook(listen="0.0.0.0",
                          port=PORT,
                          url_path=TOKEN)
    
    updater.bot.set_webhook("https://{}/{}".format(APP_NAME,TOKEN))
    #updater.bot.set_webhook(APP_NAME + TOKEN)

    updater.idle()


if __name__ == '__main__':
    main()
