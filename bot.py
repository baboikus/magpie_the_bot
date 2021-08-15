from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters

import datetime

from magpie import Magpie
from task import SEND_MESSAGE_TO, update_enviroment_loop, update_mailbox_loop
import playground

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

    SEND_MESSAGE_TO[user] = lambda m: context.bot.send_message(chat_id=update.effective_chat.id, text=m)

    print("UTC % s pushed % s <% s>: <% s>" 
          % (datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'), update.update_id, user, command))
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=magpie.request(user, command))
    print("UTC % s done   % s <% s>: <% s>" 
          % (datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'), update.update_id, user, command))

message_handler = MessageHandler(Filters.command, magpie_request)
dispatcher.add_handler(message_handler) 

magpie.init_default_event_handlers()
playground.init(magpie)

update_enviroment_loop()
update_mailbox_loop()

updater.start_polling()
updater.idle()









