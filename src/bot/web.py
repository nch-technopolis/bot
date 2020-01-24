from bottle import get, post, request

from .config import VERSION
from . import bot


@post('/bot/webhook/')
def webhook():
    update = request.json
    bot.reply(update)
    return 'OK'


@get('/bot/version/')
def version():
    return VERSION
