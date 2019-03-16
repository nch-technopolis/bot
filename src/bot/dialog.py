from queue import Queue
from threading import Thread

from .replies import IDialog


_END_MESSAGE = object()


def chatter_bot_dialog(chatterbot):

    class ChatterBotDialog(IDialog):
        def __init__(self, bot, update):
            self._bot = bot
            self._messages = Queue()
            self._chat_id = update['message']['chat']['id']
            self._chatterbot = chatterbot
            self._dialog = Thread(target=self._start)

        def start(self):
            self._dialog.start()

        def end(self):
            self._messages.put_nowait(_END_MESSAGE)

        def new_message(self, update):
            self._messages.put_nowait(update)

        def _start(self):
            while True:
                update = self._messages.get()
                if update is _END_MESSAGE:
                    return
                message = update['message']['text']
                reply = self._chatterbot.get_response(message)
                self._bot.api.send_message(chat_id=self._chat_id, text=reply)
                self._messages.task_done()

    return ChatterBotDialog
