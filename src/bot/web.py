from urllib.parse import urljoin

from bottle import post, get, request

from .api import TelegramBotAPI
from .config import API_TOKEN, WEBHOOK_PATH


def get_webhook_url(request):
    return urljoin(f'https://{request.urlparts.netloc}', WEBHOOK_PATH)


@post(WEBHOOK_PATH)
def webhook():
    return 'OK'
