from bottle import post, get

from .api import TelegramBotAPI
from .config import API_TOKEN, VERSION, WEBHOOK_PATH


@post(WEBHOOK_PATH)
def webhook():
    update = request.json
    if 'message' in update:
        message = update['message']
        text = message['text']
        if 'как дела' in text.lower():
            chat_id = message['chat']['id']
            message = 'Ленар меня предал'
            api = TelegramBotAPI(API_TOKEN)
            api.send_message(chat_id=chat_id, text=text)
    return 'OK'


@get('/bot/version/')
def version():
    return VERSION
