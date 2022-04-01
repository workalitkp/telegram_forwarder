from decouple import config
from telegram.ext import Updater, MessageHandler, Filters
from telegram import Update
from telegram.ext import CallbackContext
from telegram.ext import CommandHandler
import logging
import re
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

TOKEN = config("TOKEN", default=None)
ADMIN = config("ADMIN",default=None)
CHANNEL = config("CHANNEL",default=None)
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="hi im a forwarder bot!\nsend me your posts")


def remove_tag(caption):
    return re.sub(r'(https?:\/\/)?(www[.])?(telegram|t)\.me\/([a-zA-Z0-9_-]*)\/?','',caption)

def clean_caption(caption):
    cleaned = remove_tag(caption)
    cleaned += "\n\njoin {} \nsource: {}".format(CHANNEL,"source")
    return cleaned
def forward_post(update: Update, context: CallbackContext):
    context.bot.copy_message(chat_id=CHANNEL, from_chat_id=update.effective_chat.id, message_id=update.message.message_id,caption=clean_caption(update.message.caption))

start_handler = CommandHandler('start', start)
post_handler = MessageHandler(Filters.all & ~Filters.command, forward_post)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(post_handler)
updater.start_polling()
