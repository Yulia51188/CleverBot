import argparse
import logging
import os
import random
import vk_api

from dotenv import load_dotenv
from get_response_from_dialogflow import detect_intent_texts
from telegram import Bot
from tg_log_handler import TelegramLogsHandler
from vk_api.longpoll import VkEventType
from vk_api.longpoll import VkLongPoll


logger = logging.getLogger('verb_game_bot')


def parse_arguments():
    parser = argparse.ArgumentParser(description='Run VK bot intergrated '
        'with DialogFlow')
    parser.add_argument('--debug', action='store_true',
        help="set logger DEBUG level")
    parser.add_argument('--language_code', '-l', type=str, default='ru-RU',
        help='language code for DialogFlow agent, default is "ru-RU"')
    return parser.parse_args()


def run_smart_bot(vk_group_token, project_id, language_code='ru-RU'):
    vk_session = vk_api.VkApi(token=vk_group_token)
    longpoll = VkLongPoll(vk_session)
    vk = vk_session.get_api()
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            logger.debug(f"Новое сообщение от {event.user_id}: {event.text}")       
            send_smart_response(event, vk, project_id, language_code)


def send_smart_response(event, vk, project_id, language_code):
    response_text, is_fallback = detect_intent_texts(project_id, 
        event.user_id, [event.text], language_code)
    logger.debug(f"Fallback: {is_fallback}")
    logger.debug(f"Answer is: {response_text}")
    if not is_fallback:
        vk.messages.send(
            user_id=event.user_id,
            message=response_text,
            random_id=random.randint(1, 32767)
        )
    else:
        logger.warning(f'Fallback: VK user {event.user_id} message is not '
            f'recognized:\n{event.text}')


def main():
    args = parse_arguments()
    load_dotenv()
    
    vk_group_token = os.getenv("VK_GROUP_TOKEN")
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
    
    run_smart_bot(vk_group_token, project_id, args.language_code)


if __name__=='__main__':
    main()