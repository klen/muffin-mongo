import asyncio

import asyncio_mongo
import mock
import muffin
import pytest


@pytest.fixture(scope='session')
def app(loop):
    app = muffin.Application(
        'mongo', loop=loop,

        PLUGINS=['muffin_mongo'])

    create = asyncio_mongo.Connection.create = mock.MagicMock()
    t = asyncio.Task(asyncio.coroutine(lambda: None)())
    t.set_result(create)
    create.return_value = t

    return app


def test_muffin_mongo(app):
    assert app.ps.mongo
    assert app.ps.mongo.conn
    assert app.ps.mongo.conn.called
