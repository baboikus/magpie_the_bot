import time, threading

from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters

from magpie import Magpie
from task import run_time_machine

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

def magpie_request(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=magpie.request(update.effective_user.id, update.message.text))

# enter_handler = CommandHandler('enter', enter)
# dispatcher.add_handler(enter_handler)

# leave_handler = CommandHandler('leave', leave)
# dispatcher.add_handler(leave_handler)

# unknown_handler = MessageHandler(Filters.command, unknown)
# dispatcher.add_handler(unknown_handler)

message_handler = MessageHandler(Filters.command, magpie_request)
dispatcher.add_handler(message_handler)


def update_state_loop():
  threading.Timer(60.0, update_state_loop).start()
  run_time_machine(1.0 / 60.0) 

update_state_loop()
updater.start_polling()









