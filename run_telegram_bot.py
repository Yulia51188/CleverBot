import os
from dotenv import load_dotenv
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import Bot
from get_response_from_dialogflow import detect_intent_texts
from functools import partial
import argparse
from tg_log_handler import TelegramLogsHandler


logger = logging.getLogger('verb_game_bot')


def parse_arguments():
    parser = argparse.ArgumentParser(description='Run Telegram bot intergrated '
        'with DialogFlow')
    parser.add_argument('--debug', action='store_true',
        help="set logger DEBUG level")
    parser.add_argument('-language_code', '-l', type=str, default='ru-RU',
        help='language code for DialogFlow agent, default is "ru-RU"')
    return parser.parse_args()


def error_callback(update, context):
    logger.error('Update "%s" caused error "%s"', update, error)


def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Здравствуйте!")


def echo(bot, update):
    update.message.reply_text(update.message.text)


def answer_to_message(bot, update, project_id, language_code):
    fulfillment_text, is_fallback = detect_intent_texts(project_id, 
        update.message.chat_id, [update.message.text], language_code)
    bot.send_message(chat_id=update.message.chat_id, text=fulfillment_text)
    if is_fallback:
        logger.warning(f'Fallback: Telegram user {update.message.chat_id} '
            f'message is not recognized:\n\n{update.message.text}')


def run_bot(token, project_id, language_code='ru-RU'):
    updater = Updater(token=token)
    updater.dispatcher.add_error_handler(error_callback)  
    updater.dispatcher.add_handler(CommandHandler("start", start))
    updater.dispatcher.add_handler(
        MessageHandler(
            Filters.text, 
            partial(
                answer_to_message, 
                project_id=project_id,  
                language_code=language_code,
            )
        )
    )
    updater.start_polling()
    updater.idle()


def main():
    args = parse_arguments()
    load_dotenv()

    os.environ["GOOGLE_APPLICATION_CREDENTIALS"]=os.getenv("GOOGLE_CREDENTIALS")
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    project_id = os.getenv("PROGECT_ID")

    if args.debug:
        logging.basicConfig(format='%(asctime)s:%(name)s:%(levelname)s - '
            '%(message)s', level=logging.DEBUG)
    else:
        logging.basicConfig(format='%(asctime)s:%(name)s:%(levelname)s - '
            '%(message)s', level=logging.WARNING)     
    

    log_bot_token = os.getenv("LOG_BOT_TOKEN")
    log_bot_chat_id = os.getenv("LOG_CHAT_ID")
    tg_handler = TelegramLogsHandler(Bot(token=log_bot_token), log_bot_chat_id)
    tg_handler.setLevel(logging.WARNING) 
    logger.addHandler(tg_handler)
    
    run_bot(bot_token, project_id, args.language_code)


if __name__=='__main__':
    main()
