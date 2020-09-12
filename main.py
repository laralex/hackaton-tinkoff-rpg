from time import time
from datetime import timedelta
from telegram import (KeyboardButton, ReplyKeyboardMarkup, ChatAction)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler, PicklePersistence)

# Enable logging
import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# IMPORT OUR FILES
from auxilliary import * 
from from_example import * # example with persistent data
import pickle_jobs_handlers # for loading and saving persistent data
import inventory

# main

def main():
    # Create the Updater and pass it your bot's token.
    pp = PicklePersistence(filename='rpg-data')
    updater = Updater("1128928807:AAGphM8nn_M_W65Eg3u57uKswazhUJ00mTk", persistence=pp, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # To extract persistent data
    job_queue = updater.job_queue
    job_queue.run_repeating(pickle_jobs_handlers.save_jobs_job, timedelta(minutes=1)) # Periodically save jobs
    try:
        pickle_jobs_handlers.load_jobs(job_queue)
    except FileNotFoundError:
        # First run
        pass

    dp.add_handler(get_example_conversation_handler())

    show_data_handler = CommandHandler('show_data', show_data)
    dp.add_handler(show_data_handler)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    print("Bot is running")
    updater.idle()

    # Run again after bot has been properly shutdown
    pickle_jobs_handlers.save_jobs(job_queue)
    print("Bot is shutdown")

# NO MORE CODE

if __name__ == '__main__':
    main()