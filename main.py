from decouple import config
from telegram.ext import Updater, MessageHandler, Filters
from telegram import Update
from telegram.ext import CallbackContext
from telegram.ext import CommandHandler
from contextlib import suppress
import logging
import re

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

TOKEN = config("TOKEN", default=None)
ADMINS = config("ADMINS",default=None).split(",")
CHANNEL = config("CHANNEL",default=None)
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher


def remove_tag(caption):
    try:
        found = re.search('(https?:\/\/)?(www[.])?(telegram|t)\.me\/([a-zA-Z0-9_-]*)\/?', caption).groups()[-1]
    except AttributeError:
        found = None
    if (not found):
        try:
            found = re.search('\B@\S+', caption).group(0)[1:]
        except AttributeError:
            found = None
    caption = re.sub(r'(https?:\/\/)?(www[.])?(telegram|t)\.me\/([a-zA-Z0-9_-]*)\/?', '', caption)
    caption = re.sub(r'\B@\S+', '', caption)
    return caption,found


def clean_caption(caption):
    cleaned , source = remove_tag(caption)
    if(source):
        cleaned += "\n\njoin {} \nsource: {}".format(CHANNEL,source)
    else:
        cleaned += "\n\njoin {}".format(CHANNEL)
    return cleaned


def start(update: Update, context: CallbackContext):
    if(str(update.effective_chat.id) in ADMINS):
        context.bot.send_message(chat_id=update.effective_chat.id, text="hi im a forwarder bot!\nsend me your posts")
    else:
        context.bot.send_message(chat_id=update.effective_chat.id,text="you are not the admin of this bot!")

def forward_post(update: Update, context: CallbackContext):
    if(str(update.effective_chat.id) in ADMINS):
        context.bot.copy_message(chat_id=CHANNEL, from_chat_id=update.effective_chat.id, message_id=update.message.message_id,caption=clean_caption(update.message.caption))
    else:
        context.bot.send_message(chat_id=update.effective_chat.id,text="you are not the admin of this bot!")


def forward_text(update: Update, context: CallbackContext):
    if(str(update.effective_chat.id) in ADMINS):
        context.bot.send_message(chat_id=CHANNEL,text=clean_caption(update.message.text))
    else:
        context.bot.send_message(chat_id=update.effective_chat.id,text="you are not the admin of this bot!")


def main():
    start_handler = CommandHandler('start', start)
    post_handler = MessageHandler(Filters.all & ~Filters.command, forward_post)
    text_handler = MessageHandler(Filters.text & ~Filters.command, forward_text)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(text_handler)
    dispatcher.add_handler(post_handler)
    updater.start_polling()


if __name__ == '__main__':
    with suppress(Exception):
        main()