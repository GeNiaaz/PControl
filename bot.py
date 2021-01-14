import os
import keyboard
import json
import logging
import time
from telegram.ext import Updater, ConversationHandler, CommandHandler, MessageHandler, Filters

# JSON init
with open('data.json') as file:
    data = json.load(file)

# Bot API token and password here
TOKEN = data["TOKEN"]
Password = range(1)

# logger
logger = logging.getLogger(__name__)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def save_json ():
    with open('data.json', 'w') as f:
        json.dump(data, f)
    f.close()


# Security
def unlock (update, context):
    if data["PERMA_LOCKED"] == "1":
        str = "You are out of attempts, PControl has been locked permanently"
        context.bot.send_message(
            chat_id=update.message.chat_id, text=str, parse_mode='Markdown')
    else: 
        str = "Send the password to unlock the bot"
        context.bot.send_message(
            chat_id=update.message.chat_id, text=str, parse_mode='Markdown')
        return Password

def lock (update, context):
    if data["PERMA_LOCKED"] == "1":
        str = "You are out of attempts, PControl has been locked permanently"
        context.bot.send_message(
            chat_id=update.message.chat_id, text=str, parse_mode='Markdown')
    else: 
        if data["LOCK_STATUS"] == "1":
            str = "Bot is already locked"
            context.bot.send_message(
                chat_id=update.message.chat_id, text=str, parse_mode='Markdown')
        else: 
            str = "Bot has been locked"
            data["LOCK_STATUS"] = "1"
            data["ATTEMPTS_LEFT"] ="5"
            save_json()
            context.bot.send_message(
                chat_id=update.message.chat_id, text=str, parse_mode='Markdown')

def locked_permanently (update, context):
    str = "Bot is locked permanently, access PC to reset"
    context.bot.send_message(
        chat_id=update.message.chat_id, text=str, parse_mode='Markdown')

def password (update,context): 
    if str(update.message.text)[0] == "/": 
        msg = "Enter text, NOT a command. Please try again"
        context.bot.send_message(
            chat_id=update.message.chat_id, text=msg, parse_mode='Markdown')
        return Password
    else: 
        if update.message.text_markdown == data["PASSWORD"]:
            data["LOCK_STATUS"] = "0"
            save_json()

            msg = "PControl has been unlocked, enjoy :)"
            context.bot.send_message(
                chat_id=update.message.chat_id, text=msg, parse_mode='Markdown')
            return ConversationHandler.END
        else:
            num = int(data["ATTEMPTS_LEFT"])
            if (num > 0):
                msg = "Password is incorrect, you have " + data["ATTEMPTS_LEFT"] + " attempts left before PControl locks permanently.\n Please try again!"
                num -= 1
                str_num = str(num)
                data["ATTEMPTS_LEFT"] = str_num
                save_json()
                context.bot.send_message(
                    chat_id=update.message.chat_id, text=msg, parse_mode='Markdown')
                return Password
            else:
                msg = "You are out of attempts, PControl has been locked permanently."
                data["PERMA_LOCKED"] = "1"
                save_json()
                context.bot.send_message(
                    chat_id=update.message.chat_id, text=msg, parse_mode='Markdown')
                return ConversationHandler.END

def cancel(update, context):
    context.bot.send_message(
        chat_id=update.message.chat_id, 
        text="Action cancelled, please try again")
    return ConversationHandler.END



# Normal commands
def start (update, context):
    str = "*Welcome to the PControl bot.*\n\n" + \
        "Power controls::\n" + \
            "/sleep : PC will sleep\n" + \
                "/shutdown : PC will shutdown\n" + \
                    "Media controls::\n\n" +\
                        "/play : Pause or play\n" + \
                            "/next : Next song\n" + \
                                "/previous : Previous song\n" + \
                                    "/softer : Lower volume\n" + \
                                        "/louder : Increase volume\n" + \
                                            "/mute : Mute or Unmute"
    context.bot.send_message(
        chat_id=update.message.chat_id, text=str, parse_mode='Markdown')

def invalid (update, context):
    str = "command was invalid, please try again"
    context.bot.send_message(
            chat_id=update.message.chat_id, text=str, parse_mode='Markdown')

def shutdown (update, context):
    if data["PERMA_LOCKED"] == "1":
        str = "You are out of attempts, PControl has been locked permanently"
        context.bot.send_message(
            chat_id=update.message.chat_id, text=str, parse_mode='Markdown')
    else: 
        if data["LOCK_STATUS"] == "1":
            str = "PControl is locked, type /unlock to unlock the bot"
            context.bot.send_message(
                chat_id=update.message.chat_id, text=str, parse_mode='Markdown')
        else: 
            str = "Shutdown command has been sent"
            context.bot.send_message(
                chat_id=update.message.chat_id, text=str, parse_mode='Markdown')
            os.system("shutdown /s /t 1")

def sleep (update, context):
    if data["PERMA_LOCKED"] == "1":
        str = "You are out of attempts, PControl has been locked permanently"
        context.bot.send_message(
            chat_id=update.message.chat_id, text=str, parse_mode='Markdown')
    else: 
        if data["LOCK_STATUS"] == "1":
            str = "PControl is locked, type /unlock to unlock the bot"
            context.bot.send_message(
                chat_id=update.message.chat_id, text=str, parse_mode='Markdown')
        else: 
            str = "Sleep command has been sent"
            context.bot.send_message(
                chat_id=update.message.chat_id, text=str, parse_mode='Markdown')
            os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")

def play (update, context):
    if data["PERMA_LOCKED"] == "1":
        str = "You are out of attempts, PControl has been locked permanently"
        context.bot.send_message(
            chat_id=update.message.chat_id, text=str, parse_mode='Markdown')
    else: 
        if data["LOCK_STATUS"] == "1":
            str = "PControl is locked, type /unlock to unlock the bot"
            context.bot.send_message(
                chat_id=update.message.chat_id, text=str, parse_mode='Markdown')
        else: 
            str = "Play / Pause media command sent"
            context.bot.send_message(
                chat_id=update.message.chat_id, text=str, parse_mode='Markdown')
            keyboard.send("play/pause media")

def next (update, context):
    if data["PERMA_LOCKED"] == "1":
        str = "You are out of attempts, PControl has been locked permanently"
        context.bot.send_message(
            chat_id=update.message.chat_id, text=str, parse_mode='Markdown')
    else: 
        if data["LOCK_STATUS"] == "1":
            str = "PControl is locked, type /unlock to unlock the bot"
            context.bot.send_message(
                chat_id=update.message.chat_id, text=str, parse_mode='Markdown')
        else: 
            str = "Play / Pause media command sent"
            context.bot.send_message(
                chat_id=update.message.chat_id, text=str, parse_mode='Markdown')
            keyboard.send("next track")

def previous (update, context):
    if data["PERMA_LOCKED"] == "1":
        str = "You are out of attempts, PControl has been locked permanently"
        context.bot.send_message(
            chat_id=update.message.chat_id, text=str, parse_mode='Markdown')
    else: 
        if data["LOCK_STATUS"] == "1":
            str = "PControl is locked, type /unlock to unlock the bot"
            context.bot.send_message(
                chat_id=update.message.chat_id, text=str, parse_mode='Markdown')
        else: 
            str = "Play / Pause media command sent"
            context.bot.send_message(
                chat_id=update.message.chat_id, text=str, parse_mode='Markdown')
            keyboard.send("previous track")

def louder (update, context):
    if data["PERMA_LOCKED"] == "1":
        str = "You are out of attempts, PControl has been locked permanently"
        context.bot.send_message(
            chat_id=update.message.chat_id, text=str, parse_mode='Markdown')
    else: 
        if data["LOCK_STATUS"] == "1":
            str = "PControl is locked, type /unlock to unlock the bot"
            context.bot.send_message(
                chat_id=update.message.chat_id, text=str, parse_mode='Markdown')
        else: 
            str = "Play / Pause media command sent"
            context.bot.send_message(
                chat_id=update.message.chat_id, text=str, parse_mode='Markdown')
            count = 5
            while (count > 0):
                keyboard.send("volume up")
                count -= 1

def softer (update, context):
    if data["PERMA_LOCKED"] == "1":
        str = "You are out of attempts, PControl has been locked permanently"
        context.bot.send_message(
            chat_id=update.message.chat_id, text=str, parse_mode='Markdown')
    else: 
        if data["LOCK_STATUS"] == "1":
            str = "PControl is locked, type /unlock to unlock the bot"
            context.bot.send_message(
                chat_id=update.message.chat_id, text=str, parse_mode='Markdown')
        else: 
            str = "Play / Pause media command sent"
            context.bot.send_message(
                chat_id=update.message.chat_id, text=str, parse_mode='Markdown')
            count = 5
            while (count > 0):
                keyboard.send("volume down")
                count -= 1

def mute (update, context):
    if data["PERMA_LOCKED"] == "1":
        str = "You are out of attempts, PControl has been locked permanently"
        context.bot.send_message(
            chat_id=update.message.chat_id, text=str, parse_mode='Markdown')
    else: 
        if data["LOCK_STATUS"] == "1":
            str = "PControl is locked, type /unlock to unlock the bot"
            context.bot.send_message(
                chat_id=update.message.chat_id, text=str, parse_mode='Markdown')
        else: 
            str = "Mute command sent"
            context.bot.send_message(
                chat_id=update.message.chat_id, text=str, parse_mode='Markdown')
            keyboard.send("volume mute")


def main():
    # Create updater and pass in Bot's API token.       
    updater = Updater(TOKEN, use_context=True)
    # Get dispatcher to register handlers
    dispatcher = updater.dispatcher


    if data["PERMA_LOCKED"] == "1":
         dispatcher.add_handler(MessageHandler(Filters.text, locked_permanently))
    else: 
        # security
        dispatcher.add_handler(CommandHandler('lock', lock))

        # answer commands
        dispatcher.add_handler(CommandHandler('start', start))
        dispatcher.add_handler(CommandHandler('shutdown', shutdown))
        dispatcher.add_handler(CommandHandler('sleep', sleep))

        # audio / media
        dispatcher.add_handler(CommandHandler('play', play))
        dispatcher.add_handler(CommandHandler('next', next)) 
        dispatcher.add_handler(CommandHandler('previous', previous)) 
        dispatcher.add_handler(CommandHandler('louder', louder)) 
        dispatcher.add_handler(CommandHandler('softer', softer)) 
        dispatcher.add_handler(CommandHandler('mute', mute))
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