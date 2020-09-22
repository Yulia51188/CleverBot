import os
from dotenv import load_dotenv
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from get_response_from_dialogflow import detect_intent_texts
from functools import partial


def error_callback(update, context, logger):
    logger.warning('Update "%s" caused error "%s"', update, error)


def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Здравствуйте!")


def echo(bot, update):
    update.message.reply_text(update.message.text)


def answer_to_message(bot, update, project_id, logger, language_code):
    fulfillment_text, _is_fallback = detect_intent_texts(project_id, 
        update.message.chat_id, [update.message.text], language_code, logger)
    bot.send_message(chat_id=update.message.chat_id, text=fulfillment_text)


def run_bot(token, logger, project_id):
    updater = Updater(token=token)
    updater.dispatcher.add_error_handler(partial(error_callback, logger=logger))  
    updater.dispatcher.add_handler(CommandHandler("start", start))
    updater.dispatcher.add_handler(MessageHandler(Filters.text, 
        partial(answer_to_message, project_id=project_id, logger=logger)))
    updater.start_polling()
    updater.idle()


# def detect_intent_texts(project_id, session_id, texts, language_code, logger):
#     """Returns the result of detect intent with texts as inputs.

#     Using the same `session_id` between requests allows continuation
#     of the conversation."""

#     session_client = dialogflow.SessionsClient()
#     session = session_client.session_path(project_id, session_id)
#     for text in texts:
#         text_input = dialogflow.types.TextInput(
#             text=text, language_code=language_code)
#         query_input = dialogflow.types.QueryInput(text=text_input)
#         response = session_client.detect_intent(
#             session=session, query_input=query_input)
#         logger.debug('=' * 20)
#         logger.debug('Query text: {}'.format(response.query_result.query_text))
#         logger.debug('Detected intent: {} (confidence: {})\n'.format(
#             response.query_result.intent.display_name,
#             response.query_result.intent_detection_confidence))
#         logger.debug('Fulfillment text: {}\n'.format(
#             response.query_result.fulfillment_text)) 
#         fulfillment_text = response.query_result.fulfillment_text
#         return fulfillment_text


def main():
    load_dotenv()
    logging.basicConfig(format='%(asctime)s:%(name)s:%(levelname)s - '
        '%(message)s', level=logging.INFO)
    logger = logging.getLogger('chatbot3_logger')
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    project_id = os.getenv("PROGECT_ID")
    run_bot(bot_token, logger, project_id)


if __name__=='__main__':
    main()