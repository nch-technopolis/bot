from typing import List, AnyStr

import requests

API_ENDPOINT = 'https://api.telegram.org'


class TelegramBotAPI:
    """
    See https://core.telegram.org/bots/api
    """
    def __init__(self, token):
        self.token = token

    def _request(self, method, **kwargs) -> dict:
        url = f'{API_ENDPOINT}/bot{self.token}/{method}'
        return requests.post(url, **kwargs).json()

    def set_webhook(self, url: str, allowed_updates: List[AnyStr] = None):
        params = {'url': url, 'allowed_updates': allowed_updates}
        return self._request('setWebhook', data=params)

    def delete_webhook(self):
        return self._request('deleteWebhook')

    def send_message(self, *, chat_id, text):
        return self._request('sendMessage', chat_id=chat_id, text=text)

