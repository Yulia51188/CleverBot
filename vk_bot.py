import os
from dotenv import load_dotenv
import logging
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType


def run_longpolling(vk_group_token, logger):
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


def main():
    load_dotenv()
    logging.basicConfig(format='%(asctime)s:%(name)s:%(levelname)s - '
        '%(message)s', level=logging.DEBUG)
    logger = logging.getLogger('chatbot3_logger')
    vk_group_token = os.getenv("VK_GROUP_TOKEN")
    project_id = os.getenv("PROGECT_ID")
    run_longpolling(vk_group_token, logger)


if __name__=='__main__':
    main()