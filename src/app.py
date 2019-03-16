import bottle

from bot import web

application = bottle.default_app()

if __name__ == '__main__':
    bottle.run(host='localhost', port=9000, debug=True)

