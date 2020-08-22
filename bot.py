import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import os
from selenium import webdriver
import time

PORT = int(os.environ.get('PORT', 5000))

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
TOKEN = '1389566736:AAEzWx-Pmr6XKOsYNLwFLXQqAvujABiyfdQ'

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')
    driver = webdriver.Firefox()

    driver.get('https://www.hurryupde.com//aproducts.php')
    while True:
       time.sleep(20)
       driver.refresh()
    driver.quit()
	
    web_content = get_webpage_content('https://www.hurryupde.com//aproducts.php') # get the page source
    last_mod_time = str(get_last_modified_time(web_content)) # update when it was created last.
    hurryup_df = get_worldometer_df(web_content) # create the dataframe
    hurryup_df["mod_time"] = [last_mod_time]*hurryup_df.shape[0]

    print hurryup_df


#def help(update, context):
    """Send a message when the command /help is issued."""
    #update.message.reply_text('Help!')

#def echo(update, context):
    """Echo the user message."""
    #update.message.reply_text(update.message.text)

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    #dp.add_handler(CommandHandler("help", help))

    # on noncommand i.e message - echo the message on Telegram
    #dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=TOKEN)
    updater.bot.setWebhook('https://agile-earth-81836.herokuapp.com/' + TOKEN)

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()


def repeat_hurryup(hurryup_URL):
      web_content = get_webpage_content(hurryup_URL) # get the page source
      last_mod_time = str(get_last_modified_time(web_content)) # update when it was created last.
      hurryup_df = get_worldometer_df(web_content) # create the dataframe
      hurryup_df["mod_time"] = [last_mod_time]*hurryup_df.shape[0]