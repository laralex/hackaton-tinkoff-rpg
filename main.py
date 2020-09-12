from telegram.ext import Updater
from telegram.ext import CommandHandler

updater = Updater(token='1128928807:AAGphM8nn_M_W65Eg3u57uKswazhUJ00mTk', use_context=True)

dispatcher = updater.dispatcher




import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# handle start

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Fuck, this works!")

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

# entry point
if __name__ == "__main__":
    updater.start_polling()
