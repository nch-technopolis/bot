from bottle import post, get

from .config import VERSION, WEBHOOK_PATH


@post(WEBHOOK_PATH)
def webhook():
    return 'OK'


@get('/bot/version/')
def version():
    return VERSION
