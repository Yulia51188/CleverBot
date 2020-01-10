import os
from dotenv import load_dotenv
import logging
from telegram.ext import Updater
from telegram.error import (TelegramError, Unauthorized, BadRequest, 
                            TimedOut, ChatMigrated, NetworkError)
from telegram.ext import CommandHandler

logging.basicConfig(format='%(asctime)s:%(name)s:%(levelname)s - '
    '%(message)s', level=logging.INFO)
logger = logging.getLogger('chatbot3_logger')


def error_callback(update, context):
    logger.warning('Update "%s" caused error "%s"', update, error)
    try:
        raise context.error
    except Unauthorized:
        pass
        # remove update.message.chat_id from conversation list
    except BadRequest:
        pass
        # handle malformed requests - read more below!
    except TimedOut:
        pass
        # handle slow connection problems
    except NetworkError:
        pass
        # handle other connection problems
    except ChatMigrated as e:
        pass
        # the chat_id of a group has changed, use e.new_chat_id instead
    except TelegramError:
        pass
        # handle all other telegram related errors


def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Здравствуйте!")


def run_bot(token):
    updater = Updater(token=token)
    updater.dispatcher.add_error_handler(error_callback)
    start_handler = CommandHandler('start', start)
    updater.dispatcher.add_handler(start_handler)
    updater.start_polling()


def main():
    load_dotenv()
    bot_token = os.getenv("BOT_TOKEN")
    run_bot(bot_token)


if __name__=='__main__':
    main()