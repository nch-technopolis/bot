import random

from .api.vk import oauth_url
from .utils import Triggerable


def text_contains(*targets):
    def trigger(update):
        if not text_message(update):
            return False
        text = update['message']['text'].lower()
        for target in targets:
            if target not in text:
                return False
        return True
    return trigger


def always(*args, **kwargs):
    return True


def text_message(update):
    return 'text' in update.get('message', {})


def video_message(update):
    return 'video' in update.get('message', {})


class Reply(Triggerable):
    def handle(self, bot, update) -> bool:
        result = False
        if self.triggered(update):
            result = self.process_update(bot, update)
            if result is None:
                return True
        return result

    def process_update(self, bot, update):
        raise NotImplementedError()


class VKMixin:
    def __init__(self, vk, *args, **kwargs):
        self.vk = vk
        super().__init__(*args, **kwargs)


class RandomPhoto(VKMixin, Reply):
    def __init__(self, user_id, *args, **kwargs):
        self.user_id = user_id
        super().__init__(*args, **kwargs)

    def process_update(self, bot, update):
        chat_id = update['message']['chat']['id']

        try:
            photos = self.vk.photos.get_all(owner_id=self.user_id, count=200)

            if int(photos['response']['count']) <= 0:
                bot.api.send_message(chat_id=chat_id, text='У меня их нет')
                return
        except Exception:
            bot.api.send_message(
                chat_id=chat_id,
                text='У меня ВК не работает, ..(((',
            )
            raise

        photo = random.choice(photos['response']['items'])
        for size in photo['sizes']:
            if size['type'] == 'x':
                url = size['url']
                bot.api.send_message(chat_id=chat_id, text=url)


class VkAuth(Reply):
    def __init__(self, redirect_uri, client_id, *args, **kwargs):
        self.redirect_uri = redirect_uri
        self.client_id = client_id
        super().__init__(*args, **kwargs)

    def process_update(self, bot, update):
        chat_id = update['message']['chat']['id']
        vk_auth_url = oauth_url(self.client_id, self.redirect_uri)
        reply_markup = {
            'inline_keyboard': [[
                {'text': 'Войти', 'url': vk_auth_url},
            ]],
        }
        bot.api.send_message(
            chat_id=chat_id,
            text='Заходи',
            reply_markup=reply_markup,
        )


class RandomReply(Reply):
    def __init__(self, replies, *args, **kwargs):
        self.replies = replies
        super().__init__(*args, **kwargs)

    def process_update(self, bot, update):
        reply = random.choice(self.replies)
        chat_id = update['message']['chat']['id']
        bot.api.send_message(chat_id=chat_id, text=reply)


class IDialog:

    def start(self):
        raise NotImplementedError

    def end(self):
        raise NotImplementedError

    def new_message(self, update):
        raise NotImplementedError


class StartDialog(Reply):
    def __init__(self, start_trigger, stop_trigger, dialog_factory, *args, **kwargs):
        self._dialogs = {}
        self._dialog_factory = dialog_factory
        self._start_trigger = start_trigger
        self._stop_trigger = stop_trigger
        super().__init__(*args, **kwargs)

    def process_update(self, bot, update):
        from_user = update['message']['from']
        chat_id = update['message']['chat']['id']
        user_id = from_user['id']
        key = chat_id, user_id
        dialog = self._dialogs.get(key)

        if dialog is None:
            if self._start_trigger(update):
                dialog = self._dialog_factory(bot, update)
                dialog.start()
                self._dialogs[key] = dialog
                return True
            return False

        if self._stop_trigger(update):
            dialog.end()
            del self._dialogs[key]
        else:
            dialog.new_message(update)
