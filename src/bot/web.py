from bottle import get, post, request

from .api.vk import get_access_token
from .config import VERSION, VK_CLIENT_ID,VK_AUTH_REDIRECT_URI, VK_SECRET_KEY
from .store import save_vk_access_token, publish_update


@post('/bot/webhook/')
def webhook():
    update = request.json
    publish_update(update)
    return 'OK'


@get('/auth/callback/vk/')
def vk_auth_callback():
    code = request.params['code']
    token = get_access_token(
        client_id=VK_CLIENT_ID,
        client_secret=VK_SECRET_KEY,
        redirect_uri=VK_AUTH_REDIRECT_URI,
        code=code,
    )
    save_vk_access_token(token)
    return 'OK'


@get('/bot/version/')
def version():
    return VERSION
