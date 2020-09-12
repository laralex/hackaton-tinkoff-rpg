from time import time
from datetime import timedelta
from telegram import (KeyboardButton, ReplyKeyboardMarkup, ChatAction)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler, PicklePersistence)

from auxilliary import *
from from_example import *

import pickle_jobs_handlers # For loading of persistent data
import inventory

# Enable logging
import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# main

def main():
    # Create the Updater and pass it your bot's token.
    pp = PicklePersistence(filename='rpg-data')
    updater = Updater("1128928807:AAGphM8nn_M_W65Eg3u57uKswazhUJ00mTk", persistence=pp, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # To extract persistent data
    job_queue = updater.job_queue
    
    # Periodically save jobs
    job_queue.run_repeating(pickle_jobs_handlers.save_jobs_job, timedelta(minutes=1))

    try:
        pickle_jobs_handlers.load_jobs(job_queue)

    except FileNotFoundError:
        # First run
        pass

    # Add conversation handler with the states CHOOSING, TYPING_CHOICE and TYPING_REPLY
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            CHOOSING: [MessageHandler(Filters.regex('^(Age|Favourite colour|Number of siblings)$'),
                                      regular_choice),
                       MessageHandler(Filters.regex('^Something else...$'),
                                      custom_choice),
                       ],

            TYPING_CHOICE: [
                MessageHandler(Filters.text & ~(Filters.command | Filters.regex('^Done$')),
                               regular_choice)],

            TYPING_REPLY: [
                MessageHandler(Filters.text & ~(Filters.command | Filters.regex('^Done$')),
                               received_information)],
        },

        fallbacks=[MessageHandler(Filters.regex('^Done$'), done)],
        name="my_conversation",
        persistent=True
    )

    dp.add_handler(conv_handler)

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