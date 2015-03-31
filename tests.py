import pytest
import muffin
import mock
import asyncio_mongo
import asyncio


@pytest.fixture(scope='session')
def app(loop):
    app = muffin.Application(
        'mongo', loop=loop,

        PLUGINS=['muffin_mongo'])

    with mock.patch.object(asyncio_mongo.Connection, 'create') as create:
        t = asyncio.Task(asyncio.coroutine(lambda: None)())
        t.set_result(create)
        create.return_value = t
        loop.run_until_complete(app.start())

    return app


def test_muffin_session(app):
    assert app.ps.mongo
    assert app.ps.mongo.conn
    assert app.ps.mongo.conn.called
