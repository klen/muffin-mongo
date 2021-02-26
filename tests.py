"""The Test is require mongodb running on localhost:27017."""

import muffin
import pytest
from motor import motor_asyncio as aiomotor


@pytest.fixture
def aiolib():
    return 'asyncio'


@pytest.fixture
def app():
    return muffin.Application('example', debug=True)


async def test_mongo(app, client):
    from muffin_mongo import Plugin as Mongo

    mongo = Mongo(app, database='tests')
    assert mongo.client

    @app.route('/')
    async def test(request):
        breakpoint()
        pass

    async with client.lifespan():
        # Get a collection
        assert isinstance(mongo.items, aiomotor.AsyncIOMotorCollection)
        assert mongo.items.database.name == 'tests'

        # Clear the collection
        await mongo.items.drop()

        # Insert a document
        res = await mongo.items.insert_one({'key': 'value'})
        assert res
        assert res.inserted_id

        # Insert many
        await mongo.items.insert_many([{'key': str(n)} for n in range(10)])

        # Get a count
        total = await mongo.items.count_documents({})
        assert total == 11

        # Get a single document
        res2 = await mongo.items.find_one({'key': 'value'})
        assert res2
        assert res2['_id'] == res.inserted_id

        # Find all
        docs = await mongo.items.find().to_list(100)
        assert docs
        assert len(docs) == 11

        # Update the document
        await mongo.items.replace_one({'_id': res2['_id']}, {'key': 'value2'})
        res3 = await mongo.items.find_one({'_id': res2['_id']})
        assert res3['key'] == 'value2'


async def test_readme(app, client):
    from muffin_mongo import Plugin as Mongo

    mongo = Mongo(app, database='tests')

    @app.route('/items', methods=['GET'])
    async def get_items(request):
        """Return a JSON with items from the database."""
        documents = await mongo.items.find().sort('key').to_list(100)
        return [dict(dd.items(), _id=str(dd['_id'])) for dd in documents]

    @app.route('/items', methods=['POST'])
    async def insert_item(request):
        """Store items from JSON into database. Return ids."""
        data = await request.data()  # parse formdata/json from the request
        res = await mongo.items.insert_many(data)
        return [str(key) for key in res.inserted_ids]

    async with client.lifespan():
        await mongo.items.drop()

        res = await client.post('/items', json=[{'key': n} for n in range(10)])
        assert res.status_code == 200
        json = await res.json()
        assert json
        assert len(json) == 10

        res = await client.get('/items')
        assert res.status_code == 200
        json = await res.json()
        assert json
        assert len(json) == 10
        assert json[0]['_id']
        assert json[0]['key'] == 0
