import functools
import json
from urllib.parse import urljoin

from bottle import post, get, request

from .api import TelegramBotAPI
from .config import API_TOKEN, LOG_FILE_PATH, VERSION, WEBHOOK_PATH


def log_request(view):
    @functools.wraps(view)
    def wrapper(*args, **kwargs):
        with open(LOG_FILE_PATH, 'a') as f:
            f.write(json.dumps(request.params))
            f.wirte('\n')
        return view(*args, **kwargs)
    return wrapper


@post(WEBHOOK_PATH)
@log_request
def webhook():
    return 'OK'


@get('/bot/version/')
def version():
    return VERSION
