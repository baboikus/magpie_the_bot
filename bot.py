from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters

import datetime

from magpie import Magpie
from task import update_enviroment_loop

with open('TOKEN') as f:
    TOKEN = f.readline()

updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

magpie = Magpie()

import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def magpie_request(update, context):
    user = (update.effective_user.last_name + " " + update.effective_user.first_name, update.effective_user.id)
    command = update.message.text
    print("UTC % s pushed % s <% s>: <% s>" 
          % (datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'), update.update_id, user, command))
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=magpie.request(user, command))
    print("UTC % s done   % s <% s>: <% s>" 
          % (datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'), update.update_id, user, command))

message_handler = MessageHandler(Filters.command, magpie_request)
dispatcher.add_handler(message_handler) 

init_commands = [
        "/task_add task1 tag1 tag2",
        "/task_add task2 tag3",
        "/task_add task3 tag1 tag2 tag3"
    ]
magpie.request_list("init", init_commands)

update_enviroment_loop()
updater.start_polling()









