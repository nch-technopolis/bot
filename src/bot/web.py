from bottle import get, post, request

from .api import TelegramBotAPI
from .bot import Bot
from .config import API_TOKEN, VERSION

api = TelegramBotAPI(API_TOKEN)
bot = Bot(api)


@post('/bot/webhook/')
def webhook():
    update = request.json
    if 'message' in update:
        if 'text' in update['message']:
            bot.message_received(update['message'])
    return 'OK'


@get('/bot/version/')
def version():
    return VERSION
