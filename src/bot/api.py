from typing import List, AnyStr

import requests


class TelegramBotAPI:
    """
    See https://core.telegram.org/bots/api
    """

    ENDPOINT = 'https://api.telegram.org'

    def __init__(self, token):
        self.token = token

    def _request(self, method, **kwargs) -> dict:
        url = f'{self.ENDPOINT}/bot{self.token}/{method}'
        return requests.post(url, **kwargs).json()

    def set_webhook(self, url: str, allowed_updates: List[AnyStr] = None):
        params = {'url': url, 'allowed_updates': allowed_updates}
        return self._request('setWebhook', data=params)

    def delete_webhook(self):
        return self._request('deleteWebhook')

    def send_message(self, *, chat_id, text):
        data = {'chat_id': chat_id, 'text': text}
        return self._request('sendMessage', data=data)

