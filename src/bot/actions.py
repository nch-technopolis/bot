import datetime
import random

from .bot import Bot
from .utils import Triggerable


def at(*, weekday=None, hour=None, minute=None):
    assert any([weekday is not None, hour is not None, minute is not None])

    def trigger(*args, **kwargs):
        now = datetime.datetime.now()
        if weekday is not None:
            if now.weekday() != weekday:
                return False
        if hour is not None:
            if now.hour != hour:
                return False
        if minute is not None:
            if now.minute != minute:
                return False
        return True
    return trigger


class Action(Triggerable):
    def handle(self, bot):
        return self.triggered(bot) and self.perform(bot)

    def perform(self, bot):
        raise NotImplementedError


class SendRandomMessage(Action):
    def __init__(self, messages, *args, **kwargs):
        self._messages = messages
        super().__init__(*args, **kwargs)

    def perform(self, bot):
        text = random.choice(self._messages)
        bot.broadcast(text)


class BirthDayCongratulation(SendRandomMessage):
    def __init__(self, bdays, *args, **kwargs):
        self._bdays = bdays
        super().__init__(*args, **kwargs)

    def perform(self, bot: Bot):
        today = datetime.datetime.today()
        for bday, name in self._bdays:
            if today.day == bday.day and today.month == bday.month:
                # TODO: Don't send congratulations to all the chats
                bot.broadcast(name+'!')
                super().perform(bot)
