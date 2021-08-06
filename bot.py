from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters

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
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=magpie.request(update.effective_user.id, update.message.text))

message_handler = MessageHandler(Filters.command, magpie_request)
dispatcher.add_handler(message_handler) 

update_enviroment_loop()
updater.start_polling()









