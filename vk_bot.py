import os
from dotenv import load_dotenv
import logging
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from get_response_from_dialogflow import detect_intent_texts
import random


def run_longpolling_listener(vk_group_token, logger):
    vk_session = vk_api.VkApi(token=vk_group_token)
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            logger.debug('Новое сообщение:')
            if event.to_me:
                logger.debug(f'Для меня от: {event.user_id}')
            else:
                logger.debug(f'От меня для: {event.user_id}')
            logger.debug(f'Текст: {event.text}')


def run_longpolling_echobot(vk_group_token, logger):
    vk_session = vk_api.VkApi(token=vk_group_token)
    longpoll = VkLongPoll(vk_session)
    vk = vk_session.get_api()
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            logger.debug(f"Новое сообщение от {event.user_id}: {event.text}")
            echo(event, vk)


def run_smart_bot(vk_group_token, logger, project_id, language_code='ru-RU'):
    vk_session = vk_api.VkApi(token=vk_group_token)
    longpoll = VkLongPoll(vk_session)
    vk = vk_session.get_api()
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            logger.debug(f"Новое сообщение от {event.user_id}: {event.text}")       
            send_smart_response(event, vk, logger, project_id, language_code)


def send_smart_response(event, vk, logger, project_id, language_code):
    response_text, is_fallback = detect_intent_texts(project_id, event.user_id, [event.text], 
        language_code, logger)
    logger.debug(f"Fallback: {is_fallback}")
    logger.debug(f"Answer is: {response_text}")
    if not is_fallback:
        vk.messages.send(
            user_id=event.user_id,
            message=response_text,
            random_id=random.randint(1, 32767)
        )


def echo(event, vk):
    vk.messages.send(
        user_id=event.user_id,
        message=event.text,
        random_id=random.randint(1,1000)
    )


def main():
    logging.basicConfig(format='%(asctime)s:%(name)s:%(levelname)s - '
        '%(message)s', level=logging.DEBUG)
    logger = logging.getLogger('chatbot3_logger')
    load_dotenv()
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"]=os.getenv("GOOGLE_CREDENTIALS")
    logger.debug(os.environ['GOOGLE_APPLICATION_CREDENTIALS'])
    vk_group_token = os.getenv("VK_GROUP_TOKEN")
    project_id = os.getenv("PROGECT_ID")
    run_smart_bot(vk_group_token, logger, project_id)


if __name__=='__main__':
    main()