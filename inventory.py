from auxilliary import *
import json
from telegram import (InlineKeyboardButton, InlineKeyboardMarkup)

from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler, PicklePersistence, CallbackQueryHandler)

INVENTORY, LOOK_ITEMS, LOOK_ITEM, USE_CONSUMABLE, WEAR_EQUIPMENT, SEND_TO_FRIEND, DONE = range(7)

items_index = {}

def show_items_menu(update, title, items):
    button_list = [InlineKeyboardButton(i["name"], callback_data=i["item_id"]) for i in items]
    reply_markup = InlineKeyboardMarkup(build_menu(button_list, n_cols=2))
    update.message.reply_text(title, reply_markup=reply_markup)
    #return -1

def add_items(items, category, destination):
    for i in items:
        destination[i['item_id']] = (category, i)
        
def load_items_database():
    with open('items.json') as json_file:
        items_definitions = json.load(json_file)
        equipment = items_definitions["equipment"]
        consumables = items_definitions["consumables"]
        hats = equipment["hats"]
        costumes = equipment["costumes"]
        boots = equipment["boots"]
        rings = equipment["rings"]

        add_items(consumables, "consumables", items_index) 
        add_items(hats, "hats", items_index) 
        add_items(costumes, "costumes", items_index) 
        add_items(boots, "boots", items_index) 
        add_items(rings, "rings", items_index) 

def wear_something(update, context, inventory, category):
    items_in_inventory = [items_index[x][1] for x in inventory if items_index[x][0] == category]
    show_items_menu(update, "Все предметы категории" + category, items_in_inventory)
    #if 0 <= selected_idx < len(items_in_inventory):
       # context.user_data["equipped"]["hats"] = items_in_inventory[selected_idx]

@send_typing_action   
def enter_inventory(update, context):
    pass

def obtain_item(update, context, item_id):
    pass

@send_typing_action  
def show_inventory(update, context):
    context.user_data["inventory"] = [1, 2, 5, 10, 12]
    inventory = context.user_data["inventory"]
    #print(inventory)
    #print(items_index)
    items_in_inventory = [items_index[x][1] for x in inventory]
    show_items_menu(update, "Все ваши предметы", items_in_inventory)
    return INVENTORY 

@send_typing_action
def consume_item(update, context):
    pass

@send_typing_action
def wear_hat(update, context):
    wear_something(update, context, context.user_data['inventory'], "hats")

@send_typing_action
def wear_costume(update, context):
    wear_something(update, context, context.user_data['inventory'], "costumes")

@send_typing_action
def wear_boots(update, context):
    wear_something(update, context, context.user_data['inventory'], "boots")

@send_typing_action
def wear_ring(update, context):
    wear_something(update, context, context.user_data['inventory'], "rings")

@send_typing_action
def done(update, context):
    pass

def inspect_item(bot, update, user_data):
    print("callback: " + user_data)

def get_inventory_conversation():
    return ConversationHandler(
        entry_points=[CommandHandler('inventory', show_inventory)],

        states={
            INVENTORY: [CallbackQueryHandler(inspect_item, pass_user_data=True)],
            LOOK_ITEM: [CallbackQueryHandler(inspect_item, pass_user_data=True)]
        },

        fallbacks=[MessageHandler(Filters.regex('^Done$'), done)],
        name="my_conversation",
        persistent=True,
        #per_message=True,
    )