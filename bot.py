import os
import keyboard
import json
import logging
import time
from telegram.ext import Updater, ConversationHandler, CommandHandler, MessageHandler, Filters

# Bot API token and password here
TOKEN = ""
Password = range(1)

# JSON init
file = open('data.json')
data = json.load(file)

# lock so someone who accidentally discovered this bot wouldn't screw with u
LOCK_STATUS = True

# logger
logger = logging.getLogger(__name__)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def start (update, context):
    str = "Welcome to the PControl bot"
    context.bot.send_message(
        chat_id=update.message.chat_id, text=str, parse_mode='Markdown')


# Security
def unlock (update, context):
    str = "Send the password to unlock the bot"
    context.bot.send_message(
        chat_id=update.message.chat_id, text=str, parse_mode='Markdown')
    return Password

def lock (update, context):
    str = "Bot has been locked"
    LOCK_STATUS = True
    context.bot.send_message(
        chat_id=update.message.chat_id, text=str, parse_mode='Markdown')

def locked_permanently (update, context):
    str = "Bot is locked permanently, access PC to reset"
    context.bot.send_message(
        chat_id=update.message.chat_id, text=str, parse_mode='Markdown')

def password (update,context): 
    if update.message.text == PASSWORD:
        LOCK_STATUS = False
        str = "PControl has been unlocked, enjoy :)"
        context.bot.send_message(
            chat_id=update.message.chat_id, text=str, parse_mode='Markdown')
    else:
        if (ATTEMPTS_LEFT > 0):
            str = "Password is incorrect, you have " + ATTEMPTS_LEFT + "attempts left before PControl locks permanently.\n Please try again!"
            ATTEMPTS_LEFT += -1
            context.bot.send_message(
                chat_id=update.message.chat_id, text=str, parse_mode='Markdown')
            return password
        else:
            str = "You are out of attempts, PControl has been locked."
            PERMA_LOCKED = True
            context.bot.send_message(
                chat_id=update.message.chat_id, text=str, parse_mode='Markdown')
            return ConversationHandler.END

def cancel(update, context):
    context.bot.send_message(
        chat_id=update.message.chat_id, 
        text="PControl has not been unlocked, please try again")
    return ConversationHandler.END



# Normal commands
def invalid (update, context):
    str = "command was invalid, please try again"
    context.bot.send_message(
            chat_id=update.message.chat_id, text=str, parse_mode='Markdown')

def shutdown (update, context):
    if LOCK_STATUS:
        str = "PControl is locked, type /unlock to unlock the bot"
        context.bot.send_message(
            chat_id=update.message.chat_id, text=str, parse_mode='Markdown')
    else: 
        str = "Shutdown command has been sent"
        context.bot.send_message(
            chat_id=update.message.chat_id, text=str, parse_mode='Markdown')
        os.system("shutdown /s /t 1")

def sleep (update, context):
    if LOCK_STATUS:
        str = "PControl is locked, type /unlock to unlock the bot"
        context.bot.send_message(
            chat_id=update.message.chat_id, text=str, parse_mode='Markdown')
    else: 
        str = "Sleep command has been sent"
        context.bot.send_message(
            chat_id=update.message.chat_id, text=str, parse_mode='Markdown')
        os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")

def play (update, context):
    if LOCK_STATUS:
        str = "PControl is locked, type /unlock to unlock the bot"
        context.bot.send_message(
            chat_id=update.message.chat_id, text=str, parse_mode='Markdown')
    else: 
        str = "Play / Pause media command sent"
        context.bot.send_message(
            chat_id=update.message.chat_id, text=str, parse_mode='Markdown')
        keyboard.send("play/pause media")

def next (update, context):
    if LOCK_STATUS:
        str = "PControl is locked, type /unlock to unlock the bot"
        context.bot.send_message(
            chat_id=update.message.chat_id, text=str, parse_mode='Markdown')
    else: 
        str = "Play / Pause media command sent"
        context.bot.send_message(
            chat_id=update.message.chat_id, text=str, parse_mode='Markdown')
        keyboard.send("next track")

def previous (update, context):
    if LOCK_STATUS:
        str = "PControl is locked, type /unlock to unlock the bot"
        context.bot.send_message(
            chat_id=update.message.chat_id, text=str, parse_mode='Markdown')
    else: 
        str = "Play / Pause media command sent"
        context.bot.send_message(
            chat_id=update.message.chat_id, text=str, parse_mode='Markdown')
        keyboard.send("previous track")

def louder (update, context):
    if LOCK_STATUS:
        str = "PControl is locked, type /unlock to unlock the bot"
        context.bot.send_message(
            chat_id=update.message.chat_id, text=str, parse_mode='Markdown')
    else: 
        str = "Play / Pause media command sent"
        context.bot.send_message(
            chat_id=update.message.chat_id, text=str, parse_mode='Markdown')
        keyboard.send("volume up")

def softer (update, context):
    if LOCK_STATUS:
        str = "PControl is locked, type /unlock to unlock the bot"
        context.bot.send_message(
            chat_id=update.message.chat_id, text=str, parse_mode='Markdown')
    else: 
        str = "Play / Pause media command sent"
        context.bot.send_message(
            chat_id=update.message.chat_id, text=str, parse_mode='Markdown')
        keyboard.send("volume down")



def main():
    # Create updater and pass in Bot's API token.       
    updater = Updater(TOKEN, use_context=True)
    # Get dispatcher to register handlers
    dispatcher = updater.dispatcher

    if PERMA_LOCKED:
         locked_permanently
    else: 
        # answer commands
        dispatcher.add_handler(CommandHandler('start', start))
        dispatcher.add_handler(CommandHandler('shutdown', shutdown))
        dispatcher.add_handler(CommandHandler('sleep', sleep))
        # dispatcher.add_handler(CommandHandler('sleep5', sleep5))
        dispatcher.add_handler(CommandHandler('play', play))
        dispatcher.add_handler(CommandHandler('next', next)) # "next track"
        dispatcher.add_handler(CommandHandler('previous', previous)) # "previous track"
        dispatcher.add_handler(CommandHandler('louder', louder)) # "volume up"
        dispatcher.add_handler(CommandHandler('softer', softer)) # "volume down"
        # dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), invalid))

        conv_handler = ConversationHandler(
            entry_points=[CommandHandler("unlock", unlock)],
            states={
                Password : [MessageHandler(filters=None, callback=password)],
            },
            fallbacks=[CommandHandler("cancel", cancel)]
        )

        dispatcher.add_handler(conv_handler)

        # log all errors
        dispatcher.add_error_handler(error)


        # CODE TO RUN LOCALLY
        updater.start_polling()
        updater.idle()

if __name__ == '__main__':
    main()

    
# event = keyboard.record("esc")
# print(event)