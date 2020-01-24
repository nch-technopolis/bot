import json
from typing import List, AnyStr

import requests


class TelegramAPIError(Exception):
    pass


class API:
    """
    See https://core.telegram.org/bots/api
    """

    ENDPOINT = 'https://api.telegram.org'

    APIError = TelegramAPIError

    def __init__(self, token):
        self.token = token

    def _request(self, method, **kwargs) -> dict:
        url = f'{self.ENDPOINT}/bot{self.token}/{method}'
        response = requests.post(url, **kwargs).json()
        if not response['ok']:
            raise self.APIError(response['description'])
        return response

    def set_webhook(self, url: str, allowed_updates: List[AnyStr] = None):
        params = {'url': url, 'allowed_updates': allowed_updates}
        return self._request('setWebhook', data=params)

    def delete_webhook(self):
        return self._request('deleteWebhook')

    def send_message(self, *, chat_id, text, reply_markup=None):
        if not text and not reply_markup:
            return
        if reply_markup:
            reply_markup = json.dumps(reply_markup)
        data = {'chat_id': chat_id, 'text': text, 'reply_markup': reply_markup}
        return self._request('sendMessage', data=data)
