"""The Test is require mongodb running on localhost:27017."""

import muffin
import pytest


@pytest.fixture
def app():
    return muffin.Application('example', debug=True)


@pytest.mark.asyncio
async def test_mongo(app, client):
    from muffin_mongo import Plugin as Mongo

    mongo = Mongo(app, database='tests')
    assert not mongo.client

    @app.route('/')
    async def test(request):
        breakpoint()
        pass

    async with client.lifespan():
        assert mongo.client, 'Client must to be initialize after startup'
        breakpoint()


#  @pytest.fixture
#  def app():
    #  return muffin.Application('mongo')

    #  create = asyncio_mongo.Connection.create = mock.MagicMock()
    #  t = asyncio.Task(asyncio.coroutine(lambda: None)())
    #  t.set_result(create)
    #  create.return_value = t

    #  return app


#  def test_muffin_mongo(app):
    #  assert app.ps.mongo
    #  assert app.ps.mongo.conn
    #  assert app.ps.mongo.conn.called
