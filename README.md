# CleverBot
Bot with a speech recognition support for a  training course Devman (project 3, module Chatbots)
Try it, writing to: Telegram channel @Verb_game_support_bot or [VK group](https://vk.com/public198736597), because bots are deployed on [Heroku](heroku.com) and are available rigth now!

![tg_bot_demo](https://github.com/Yulia51188/CleverBot/blob/master/tg_bot_demo_2.gif) ![vk_bot_demo](https://github.com/Yulia51188/CleverBot/blob/master/vk_bot_demo_3.gif)

# About
Telegram and VK bots are integrated with service [DialogFlow](https://cloud.google.com/dialogflow/). Dialogflow CX is an advanced development suite for creating conversational AI applications, including chatbots, voicebots, and IVR bots. You can train DialogFlow agent via script `agent_education.py`. And then use the agent via API with Telegram, or VK bot, or both at the same time.

# How to install
To customize bots you need some keys that are:
- `TELEGRAM_BOT_TOKEN`: create your own bot writing to BotFather @BotFather
- `LOG_CHAT_ID`, `LOG_BOT_TOKEN`: Telegram chat id and token for support team
- `PROGECT_ID`, `GOOGLE_APPLICATION_CREDENTIALS`: create your project and agent in [DialogFlow](https://cloud.google.com/dialogflow/es/docs/quick/setup)
- `VK_GROUP_TOKEN`: create your group with bot in [VK](https://vk.com/dev/bots)

Python 3 should be already installed. Then use pip3 (or pip) to install dependencies:

```bash
pip3 install -r requirements.txt
```

# How to launch
The Example of launch in Ubuntu is:

```bash
$ python3 agent_education.py TrainingPhrases.json 
$ python3 run_telegram_bot.py 
$ python3 vk_bot.py 
```
Training phrases file example:
```json
{
    "Устройство на работу": {
        "questions": [
            "Как устроиться к вам на работу?",
            "Как устроиться к вам?",
            "Как работать у вас?",
            "Хочу работать у вас",
            "Возможно-ли устроиться к вам?",
            "Можно-ли мне поработать у вас?",
            "Хочу работать редактором у вас"
        ],
        "answer": "Если вы хотите устроиться к нам, напишите на почту game-of-verbs@gmail.com мини-эссе о себе и прикрепите ваше портфолио."
    }
  }
  ```
It is better to launch the script on a remote server, [Heroku](https://devcenter.heroku.com/articles/how-heroku-works), for example. It provides that it will work around the clock. A "Procfile" is need to launch correctly on Heroku.

# Project Goals

The code is written for educational purposes on online-course for web-developers dvmn.org, module [Chat Bots with Python](https://dvmn.org/modules/chat-bots/lesson/support-bot).
