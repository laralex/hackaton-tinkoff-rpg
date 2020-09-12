from auxilliary import *
from telegram import (KeyboardButton, ReplyKeyboardMarkup, ChatAction)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler, PicklePersistence)

CHOOSING, TYPING_REPLY, TYPING_CHOICE = range(3)

reply_keyboard = [['Age', 'Favourite colour'],
                  ['Number of siblings', 'Something else...'],
                  ['Done']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)


def facts_to_str(user_data):
    facts = list()

    for key, value in user_data.items():
        facts.append('{} - {}'.format(key, value))

    return "\n".join(facts).join(['\n', '\n'])

@send_typing_action
def start(update, context):
    # location_keyboard = KeyboardButton(text="send_location", request_location=True)
    # contact_keyboard = KeyboardButton(text="send_contact", request_contact=True)
    # custom_keyboard = [[ location_keyboard, contact_keyboard ]]
    # reply_markup = ReplyKeyboardMarkup(custom_keyboard)
    # update.message.reply_text("Would you mind sharing your location and contact with me?", reply_markup=reply_markup)

    reply_text = "Hi! My name is Doctor Botter."
    if context.user_data:
        reply_text += " You already told me your {}. Why don't you tell me something more " \
                      "about yourself? Or change anything I " \
                      "already know.".format(", ".join(context.user_data.keys()))
    else:
        reply_text += " I will hold a more complex conversation with you. Why don't you tell me " \
                      "something about yourself?"

   
    update.message.reply_text(reply_text, reply_markup=markup)

    return CHOOSING

@send_typing_action
def regular_choice(update, context):
    text = update.message.text.lower()
    context.user_data['choice'] = text
    if context.user_data.get(text):
        reply_text = 'Your {}, I already know the following ' \
                     'about that: {}'.format(text, context.user_data[text])
    else:
        reply_text = 'Your {}? Yes, I would love to hear about that!'.format(text)
    update.message.reply_text(reply_text)

    return TYPING_REPLY

@send_typing_action
def custom_choice(update, context):
    update.message.reply_text('Alright, please send me the category first, '
                              'for example "Most impressive skill"')

    return TYPING_CHOICE

@send_typing_action
def received_information(update, context):
    text = update.message.text
    category = context.user_data['choice']
    context.user_data[category] = text.lower()
    del context.user_data['choice']

    update.message.reply_text("Neat! Just so you know, this is what you already told me:"
                              "{}"
                              "You can tell me more, or change your opinion on "
                              "something.".format(facts_to_str(context.user_data)),
                              reply_markup=markup)

    return CHOOSING

@send_typing_action
def show_data(update, context):
    update.message.reply_text("This is what you already told me:"
                              "{}".format(facts_to_str(context.user_data)))

@send_typing_action
def done(update, context):
    if 'choice' in context.user_data:
        del context.user_data['choice']

    update.message.reply_text("I learned these facts about you:"
                              "{}"
                              "Until next time!".format(facts_to_str(context.user_data)))
    return ConversationHandler.END