import random
import datetime
import xml.etree.ElementTree as ET

import requests

from .config import API_TOKEN
from .telegram import API


telegram = API(API_TOKEN)


def get_dollar_rate(date):
    api_url = 'http://www.cbr.ru/scripts/XML_daily.asp'
    response = requests.get(api_url, {'date_req': date.strftime('%d/%m/%Y')})
    response.raise_for_status()
    root = ET.fromstring(response.text)
    for currency in root:
        if currency.attrib['ID'] == 'R01235':  # US dollar ID
            return currency.find('Value').text


def tell_tale():
    parts = [
        ['Внимение,', 'Срочно,', 'Привет, ребят,'],
        ['мне', 'нам'],
        ['тут только что'],
        ['позвонил', 'написал'],
        ['знакомый из министерства', 'знакомый хирург', 'брат', 'дядя', 'отец', 'родственник из Сибири'],
        ['и попросил'],
        ['никому не говорить', 'рассказать всем'],
        ['о том, что реальная информация'],
        ['скрывается', 'преувеличивается'],
        ['и в скором времени'],
        ['пизда.', 'не пизда.'],
        ['\nhttps://vademec.ru/upload/iblock/c5a/c5a908fcfd36b308bc55686202c881d6.jpg'],
    ]
    return ' '.join(random.choice(part) for part in parts)


def reply(update):
    chat_id = update['message']['chat']['id']
    text = update['message'].get('text')
    if text == 'Эй, Денис!':
        telegram.send_message(chat_id=chat_id, text='Я тут')
    elif text == 'Денис, какой курс доллара?':
        date = datetime.date.today()
        try:
            dollar_rate = get_dollar_rate(date)
            message = f'{dollar_rate} руб.'
        except:
            message = 'Не знаю'
        telegram.send_message(chat_id=chat_id, text=message)
    elif text == 'Денис, что слышно про коронавирус?':
        telegram.send_message(chat_id=chat_id, text=tell_tale())
