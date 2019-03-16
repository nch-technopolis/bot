import time
from abc import ABC, abstractmethod
from threading import Thread

from .bot import Bot
from .store import get_update


class Runner(ABC):
    def __init__(self, bot: Bot, period=60):
        self._bot = bot
        self._period = period
        self._worker = Thread(target=self.background)

    def run(self):
        self._worker.start()
        while True:
            update = self.get_update()
            self._bot.handle_update(update)

    def background(self):
        while True:
            self._bot.act()
            time.sleep(60)

    @abstractmethod
    def get_update(self):
        raise NotImplementedError


class StoredRunner(Runner):
    def get_update(self):
        update = None
        while update is None:
            time.sleep(0.5)
            update = get_update()
        return update
