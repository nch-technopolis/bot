import requests

from urllib.parse import urlencode

OAUTH_AUTH_ENDPOINT = 'https://oauth.vk.com/authorize'
OAUTH_TOKEN_ENDPOINT = 'https://oauth.vk.com/access_token'


def oauth_url(client_id, redirect_uri, display='page', scope=4):
    query = urlencode({
        'redirect_uri': redirect_uri,
        'client_id': client_id,
        'display': display,
        'scope': scope,
        'v': API.V,
        'response_type': 'code',
    })
    return f'{OAUTH_AUTH_ENDPOINT}?{query}'


def get_access_token(client_id, client_secret, redirect_uri, code):
    query = urlencode({
        'client_id': client_id,
        'client_secret': client_secret,
        'redirect_uri': redirect_uri,
        'code': code,
    })
    return requests.get(f'{OAUTH_TOKEN_ENDPOINT}?{query}').json()


class Section:
    def __init__(self, api):
        self.api = api


class Accounts(Section):
    def get_info(self):
        return self.api.request('account.getInfo')


class Photos(Section):
    def get_all(self, *, owner_id, count=20, no_service_albums=0, offset=0):
        return self.api.request(
            'photos.getAll',
            owner_id=owner_id,
            count=count,
            offset=offset,
            no_service_albums=no_service_albums,
        )


class Mount:
    def __init__(self, section):
        self.section = section

    def __get__(self, instance, owner):
        return self.section(instance)


class API:
    V = 5.92
    ENDPOINT = 'https://api.vk.com/method'

    account = Mount(Accounts)
    photos = Mount(Photos)

    def __init__(self, access_token):
        self.access_token = access_token

    def request(self, method, **kwargs):
        url = f'{self.ENDPOINT}/{method}'
        kwargs.update({'access_token': self.access_token, 'v': self.V})
        return requests.post(url, data=kwargs).json()
