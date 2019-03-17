import bottle

from .. import web


def test_application():
    assert bottle.default_app()

