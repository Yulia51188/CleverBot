import telegram
import os
from dotenv import load_dotenv


def main():
    load_dotenv()
    bot_token = os.getenv("BOT_TOKEN")


if __name__=='__main__':
    main()