from bottle import get, post, request

from .api import TelegramBotAPI
from .config import API_TOKEN, VERSION, WEBHOOK_PATH


@post(WEBHOOK_PATH)
def webhook():
    update = request.json
    if 'message' in update:
        message = update['message']
        text = message['text'].lower()
        if 'денис' in text and 'как дела' in text:
            chat_id = message['chat']['id']
            text = 'Ленар меня предал'
            TelegramBotAPI(API_TOKEN).send_message(chat_id=chat_id, text=text)
    return 'OK'


@get('/bot/version/')
def version():
    return VERSION
