from unittest.mock import MagicMock

from ..bot import Bot
from ..api.vk import oauth_url
from ..replies import VkAuth, RandomPhoto, RandomReply, text_contains


def test_vk_auth():
    redirect_uri = 'https://my.domain.com/callback/'
    client_id = 'foobar'
    bot_api = MagicMock()
    bot = Bot(
        bot_api,
        chats=set(),
        replies=[
            VkAuth(
                redirect_uri,
                client_id,
                trigger=text_contains('денис', 'дай зайти в вк'),
            ),
        ],
    )
    update = {
        'message': {
            'text': 'Денис, дай зайти в вк',
            'chat': {'id': 42},
        },
    }
    bot.handle_update(update)
    bot_api.send_message.assert_called_once()
    bot_api.send_message.assert_called_with(
        chat_id=42,
        text='Заходи',
        reply_markup={
            'inline_keyboard': [[
                {'text': 'Войти', 'url': oauth_url(client_id, redirect_uri)},
            ]]
        },
    )


def test_random_photo():
    vk = MagicMock()
    bot_api = MagicMock()

    vk.photos.get_all.return_value = {
        'response': {
            'count': 0,
            'items': [],
        },
    }

    bot = Bot(
        bot_api,
        chats=set(),
        replies=[
            RandomPhoto(1234, vk, trigger=text_contains('денис')),
        ],
    )
    bot.handle_update({
        'message': {
            'text': 'Денис, скинь фотку',
            'chat': {'id': 42},
        },
    })
    bot_api.send_message.assert_called_with(chat_id=42, text='У меня их нет')

    vk.photos.get_all.return_value = {
        'response': {
            'count': 1,
            'items': [
                {'album_id': -6,
                 'date': 1552318105,
                 'id': 456241467,
                 'owner_id': 5561827,
                 'post_id': 11617,
                 'sizes': [{'height': 87,
                            'type': 'm',
                            'url': 'https://pp.userapi.com/c856132/v856132803/43f/Oovp0RwR19I.jpg',
                            'width': 130},
                           {'height': 87,
                            'type': 'o',
                            'url': 'https://pp.userapi.com/c856132/v856132803/444/7ApT9c_FLxY.jpg',
                            'width': 130},
                           {'height': 133,
                            'type': 'p',
                            'url': 'https://pp.userapi.com/c856132/v856132803/445/rcevadaVOlw.jpg',
                            'width': 200},
                           {'height': 213,
                            'type': 'q',
                            'url': 'https://pp.userapi.com/c856132/v856132803/446/qkXqk9FTcA0.jpg',
                            'width': 320},
                           {'height': 340,
                            'type': 'r',
                            'url': 'https://pp.userapi.com/c856132/v856132803/447/pm0m7S92XqM.jpg',
                            'width': 510},
                           {'height': 50,
                            'type': 's',
                            'url': 'https://pp.userapi.com/c856132/v856132803/43e/l429b_cBhvQ.jpg',
                            'width': 75},
                           {'height': 1365,
                            'type': 'w',
                            'url': 'https://pp.userapi.com/c856132/v856132803/443/UZB7w2gPWx8.jpg',
                            'width': 2048},
                           {'height': 403,
                            'type': 'x',
                            'url': 'https://pp.userapi.com/c856132/v856132803/440/LAZ1irJ-0MU.jpg',
                            'width': 604},
                           {'height': 538,
                            'type': 'y',
                            'url': 'https://pp.userapi.com/c856132/v856132803/441/p8eACoXJ4RU.jpg',
                            'width': 807},
                           {'height': 853,
                            'type': 'z',
                            'url': 'https://pp.userapi.com/c856132/v856132803/442/l2FsGGQRRok.jpg',
                            'width': 1280}],
                 'text': ''},
            ],
        },
    }

    bot.handle_update({
        'message': {
            'text': 'Денис, скинь фотку',
            'chat': {'id': 42},
        },
    })

    bot_api.send_message.assert_called_with(
        chat_id=42,
        text='https://pp.userapi.com/c856132/v856132803/440/LAZ1irJ-0MU.jpg',
    )


def test_random_reply():
    bot_api = MagicMock()
    bot = Bot(
        bot_api,
        chats=set(),
        replies=[
            RandomReply(
                replies=['ответ', 'случайный'],
                trigger=text_contains('денис'),
            ),
        ],
    )
    update = {'message': {'text': 'ignore', 'chat': {'id': 42}}}
    bot.handle_update(update)
    bot_api.send_message.assert_not_called()

    update = {'message': {'text': 'денис, как дела?', 'chat': {'id': 42}}}
    bot.handle_update(update)
    bot_api.send_message.assert_called_once()
