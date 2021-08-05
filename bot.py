from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters

from magpie import Magpie

with open('TOKEN') as f:
    TOKEN = f.readline()

updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

magpie = Magpie()

import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def enter(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
    						 text="I'm the magpie! You are entering the forest!")

def leave(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
    						 text="I'm the magpie! You are leaving the forest! Don't forget to write down all your today doings!")

def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
    						 text="I'm the magpie! Sorry, I didn't understand that command. Please use /enter and /leave commands!")

def add_task(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=magpie.request("/task_add task1 tag1 tag2"))

def backlog(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=magpie.request("/backlog"))

def magpie_request(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=magpie.request(update.message.text))


# enter_handler = CommandHandler('enter', enter)
# dispatcher.add_handler(enter_handler)

# leave_handler = CommandHandler('leave', leave)
# dispatcher.add_handler(leave_handler)

# unknown_handler = MessageHandler(Filters.command, unknown)
# dispatcher.add_handler(unknown_handler)

# add_task_handler = CommandHandler('task_add', add_task)
# dispatcher.add_handler(add_task_handler)

# backlog_handler = CommandHandler('backlog', backlog)
# dispatcher.add_handler(backlog_handler)

message_handler = MessageHandler(Filters.command, magpie_request)
dispatcher.add_handler(message_handler)

updater.start_polling()









