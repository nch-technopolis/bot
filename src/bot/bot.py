from .config import API_TOKEN
from .telegram import API


telegram = API(API_TOKEN)


def reply(update):
    chat_id = update['message']['chat']['id']
    text = update['message'].get('text')
    if text == 'Эй, Денис!':
        telegram.send_message(chat_id=chat_id, text='Я тут')
