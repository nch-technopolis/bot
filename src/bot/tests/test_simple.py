import bottle

from .. import web
from .. runner import StoredRunner


def test_application():
    assert bottle.default_app()
