import logging
#save your token in file bot_token
from bot_token import API_TOKEN

from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler, PollAnswerHandler)

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

#Entrance poll questions
EQ0, EQ1, EQ2 = range(3)

def start(update, context):
    update.message.reply_text(
        'Привет! \n\n'
        'Пришлите /create, чтобы создать своего пресонажа.\n'
        'Пришлите /cancel, чтобы прекратить диалог.'
    )

def help(update, context):
    update.message.reply_text(
        'Пришлите /create, чтобы создать своего пресонажа.\n\n'
        'Пришлите /cancel, чтобы прекратить диалог.'
    )

def create(update, context):
    update.message.reply_text(
        'Чтобы создать своего персонажа, пожалуйста, '
        'ответьте на несколько вопросов о себе.'
    )

    variants = [['Достаточно много'], ['Не очень много'], ['Мало'], ['Пропустить']]
    update.message.reply_text(
        'Как много времени вы проводите в социальных сетях?',
        reply_markup=ReplyKeyboardMarkup(variants, one_time_keyboard=True)
    )
    payload = {0: {"variants": variants, "message_id": update.message.message_id,
                                 "chat_id": update.effective_chat.id}}
    context.bot_data.update(payload)
    return EQ0

def q0(update, context):
    context.bot_data[0]["answer"] = update.message.text
    variants = [['Да'], ['Нет'], ['Пропустить']]
    update.message.reply_text(
        'Вы инвестируете в акции?',
        reply_markup=ReplyKeyboardMarkup(variants, one_time_keyboard=True)
    )
    payload = {1: {"variants": variants, "message_id": update.message.message_id,
                                 "chat_id": update.effective_chat.id}}
    context.bot_data.update(payload)
    return EQ1

def q1(update, context):
    context.bot_data[1]["answer"] = update.message.text
    variants = [['Из дома'], ['В офисе'], ['Пропустить']]
    update.message.reply_text(
        'Вы работаете из дома или в офисе?',
        reply_markup=ReplyKeyboardMarkup(variants, one_time_keyboard=True)
    )
    payload = {2: {"variants": variants, "message_id": update.message.message_id,
                                 "chat_id": update.effective_chat.id}}
    context.bot_data.update(payload)
    return EQ2

def q2(update, context):
    context.bot_data[2]["answer"] = update.message.text
    update.message.reply_text(
        'Спасибо! Ваши ответы сохранены и будут использованы'
        'для подбора персональных заданий и бонусов!',
        reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END

def cancel(update, context):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text('Пока! Надеюсь, мы сможем пообщаться позже.',
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


def main():
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(API_TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("cancel", cancel))
    dp.add_handler(CommandHandler("help", help))

    entrance_poll_handler = ConversationHandler(
        entry_points=[CommandHandler('create', create)],

        states={
            EQ0: [MessageHandler(Filters.all, q0)],
            EQ1: [MessageHandler(Filters.all, q1)],
            EQ2: [MessageHandler(Filters.all, q2)]
        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dp.add_handler(entrance_poll_handler)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
