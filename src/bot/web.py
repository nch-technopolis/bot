from urllib.parse import urljoin

from bottle import post, get, request

from .api import TelegramBotAPI
from .config import API_TOKEN, VERSION, WEBHOOK_PATH


@post(WEBHOOK_PATH)
def webhook():
    return 'OK'


@get('/bot/version/')
def version():
    return VERSION
