from datetime import date
from unittest.mock import MagicMock, call

import freezegun
import pytest

from ..actions import BirthDayCongratulation, SendRandomMessage, at
from ..bot import Bot

always = lambda *args, **kwargs: True


def test_send_random_message():
    api = MagicMock()
    messages = ('Foo', 'Bar', 'Baz')
    actions = [SendRandomMessage(messages, trigger=always)]
    bot = Bot(api, chats={42}, actions=actions)
    bot.act()

    api.send_message.assert_called_once()
    _, kwargs = api.send_message.call_args
    assert kwargs['text'] in messages
    assert kwargs['chat_id'] == 42


def test_bday():
    api = MagicMock()
    messages = ('Happy BDay!',)
    bdays = [(date(2019, 3, 16), 'DenisBot')]
    actions = [
        BirthDayCongratulation(
            bdays,
            messages=messages,
            trigger=at(hour=10, minute=10),
        ),
    ]
    bot = Bot(api, chats={42}, actions=actions)

    with freezegun.freeze_time('2019-03-15 10:10'):
        bot.act()

    api.send_message.assert_not_called()

    with freezegun.freeze_time('2019-03-16 10:10'):
        bot.act()

    api.send_message.assert_has_calls([
        call(text='DenisBot!', chat_id=42),
        call(text='Happy BDay!', chat_id=42),
    ])


def test_at():
    with pytest.raises(AssertionError):
        at()

    trigger = at(minute=10)

    with freezegun.freeze_time('2019-06-06 10:00'):
        assert not trigger()
    with freezegun.freeze_time('2019-05-07 10:10'):
        assert trigger()
    with freezegun.freeze_time('2019-04-07 11:10'):
        assert trigger()
    with freezegun.freeze_time('2019-05-06 11:11'):
        assert not trigger()

    trigger = at(hour=10)
    with freezegun.freeze_time('2019-06-06 10:00'):
        assert trigger()
    with freezegun.freeze_time('2019-05-07 10:10'):
        assert trigger()
    with freezegun.freeze_time('2019-04-07 11:10'):
        assert not trigger()
    with freezegun.freeze_time('2019-05-06 11:11'):
        assert not trigger()

    trigger = at(weekday=0)
    with freezegun.freeze_time('2019-04-08 10:00'):
        assert trigger()
    with freezegun.freeze_time('2019-04-08 11:02'):
        assert trigger()
    with freezegun.freeze_time('2019-04-07 11:10'):
        assert not trigger()
    with freezegun.freeze_time('2019-03-06 11:11'):
        assert not trigger()

    trigger = at(hour=16, minute=20)
    with freezegun.freeze_time('2019-04-08 16:20'):
        assert trigger()
    with freezegun.freeze_time('2019-04-09 16:20'):
        assert trigger()
    with freezegun.freeze_time('2019-04-09 16:21'):
        assert not trigger()

    trigger = at(weekday=4, hour=16, minute=20)
    with freezegun.freeze_time('2019-04-05 16:20'):
        assert trigger()
    with freezegun.freeze_time('2019-04-05 16:21'):
        assert not trigger()
    with freezegun.freeze_time('2019-04-05 17:20'):
        assert not trigger()
    with freezegun.freeze_time('2019-04-06 16:20'):
        assert not trigger()
