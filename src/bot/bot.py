from contextlib import suppress


class Chats:
    def add(self, chat_id):
        raise NotImplementedError

    def remove(self, chat_id):
        raise NotImplementedError

    def __iter__(self):
        raise NotImplementedError


class Bot:
    def __init__(self, api, chats: Chats, username='', replies=(), actions=()):
        self.username = username
        self.api = api
        self.replies = replies
        self.actions = actions
        self.chats = chats

    def broadcast(self, text):
        for chat_id in self.chats:
            try:
                self.api.send_message(chat_id=chat_id, text=text)
            except self.api.APIError:
                self.chats.remove(chat_id)

    def handle_update(self, update):
        with suppress(KeyError):
            chat_id = update['message']['chat']['id']
            self.chats.add(chat_id)
        for reply in self.replies:
            if reply.handle(self, update):
                return

    def act(self):
        for action in self.actions:
            action.handle(self)
