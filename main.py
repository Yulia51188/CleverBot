import os
from dotenv import load_dotenv
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
# from telegram.error import (TelegramError, Unauthorized, BadRequest, 
#                             TimedOut, ChatMigrated, NetworkError)
from functools import partial
import dialogflow_v2 as dialogflow


def error_callback(update, context, logger):
    logger.warning('Update "%s" caused error "%s"', update, error)
    # try:
    #     raise context.error
    # except Unauthorized:
    #     pass
    #     # remove update.message.chat_id from conversation list
    # except BadRequest:
    #     pass
    #     # handle malformed requests - read more below!
    # except TimedOut:
    #     pass
    #     # handle slow connection problems
    # except NetworkError:
    #     pass
    #     # handle other connection problems
    # except ChatMigrated as e:
    #     pass
    #     # the chat_id of a group has changed, use e.new_chat_id instead
    # except TelegramError:
    #     pass
    #     # handle all other telegram related errors


def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Здравствуйте!")


def echo(bot, update):
    update.message.reply_text(update.message.text)


def smart_greating(bot, update, project_id, language_code='ru-RU'):
    fulfillment_text = detect_intent_texts(project_id, 
        update.message.chat_id, [update.message.text], language_code)
    bot.send_message(chat_id=update.message.chat_id, text=fulfillment_text)


def run_bot(token, logger, project_id):
    updater = Updater(token=token)
    updater.dispatcher.add_error_handler(partial(error_callback, logger=logger))  
    updater.dispatcher.add_handler(CommandHandler("start", start))
    updater.dispatcher.add_handler(MessageHandler(Filters.text, 
        partial(smart_greating, project_id=project_id)))
    updater.start_polling()
    updater.idle()


def detect_intent_texts(project_id, session_id, texts, language_code, logger):
    """Returns the result of detect intent with texts as inputs.

    Using the same `session_id` between requests allows continuation
    of the conversation."""

    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(project_id, session_id)
    # print('Session path: {}\n'.format(session))

    for text in texts:
        text_input = dialogflow.types.TextInput(
            text=text, language_code=language_code)

        query_input = dialogflow.types.QueryInput(text=text_input)

        response = session_client.detect_intent(
            session=session, query_input=query_input)

        logger.debug('=' * 20)
        logger.debug('Query text: {}'.format(response.query_result.query_text))
        logger.debug('Detected intent: {} (confidence: {})\n'.format(
            response.query_result.intent.display_name,
            response.query_result.intent_detection_confidence))
        logger.debug('Fulfillment text: {}\n'.format(
            response.query_result.fulfillment_text)) 
        # intent_name = response.query_result.intent.display_name
        fulfillment_text = response.query_result.fulfillment_text

        return fulfillment_text


def main():
    load_dotenv()
    logging.basicConfig(format='%(asctime)s:%(name)s:%(levelname)s - '
        '%(message)s', level=logging.DEBUG)
    logger = logging.getLogger('chatbot3_logger')
    bot_token = os.getenv("BOT_TOKEN")
    project_id = os.getenv("PROGECT_ID")
    print(project_id)
    session_id = '123456789'
    texts = ['Добрый день']
    language_code = 'en-US'
    run_bot(bot_token, logger, project_id)
    detect_intent_texts(project_id, session_id, texts, language_code)


if __name__=='__main__':
    main()