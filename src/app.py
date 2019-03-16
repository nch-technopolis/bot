import bottle

from bot import web  # noqa
from bot.config import SENTRY_SDK_KEY, VERSION

if __name__ == '__main__':
    bottle.run(host='localhost', port=9000, debug=True)
else:
    import sentry_sdk
    from sentry_sdk.integrations.wsgi import SentryWsgiMiddleware

    sentry_sdk.init(SENTRY_SDK_KEY, release=VERSION)
    app = bottle.default_app()
    app.catchall = False
    application = SentryWsgiMiddleware(app)
