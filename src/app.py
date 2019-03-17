import bottle

from bot import web

if __name__ == '__main__':
    bottle.run(host='localhost', port=9000, debug=True)
else:
    import sentry_sdk
    from sentry_sdk.integrations.wsgi import SentryWsgiMiddleware

    sentry_sdk.init("https://f7ebbcbe9cfe4d3fbbc86b353081003b@sentry.io/1417397")
    application = SentryWsgiMiddleware(bottle.default_app())

