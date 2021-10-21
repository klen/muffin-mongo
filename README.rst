Muffin-Mongo
############

.. _description:

Muffin-Mongo -- MongoDB support for Muffin_ framework.

.. _badges:

.. image:: https://github.com/klen/muffin-mongo/workflows/tests/badge.svg
    :target: https://github.com/klen/muffin-mongo/actions
    :alt: Tests Status

.. image:: https://img.shields.io/pypi/v/muffin-mongo
    :target: https://pypi.org/project/muffin-mongo/
    :alt: PYPI Version

.. image:: https://img.shields.io/pypi/pyversions/muffin-mongo
    :target: https://pypi.org/project/muffin-mongo/
    :alt: Python Versions

.. _contents:

.. contents::

.. _requirements:

Requirements
=============

- python >= 3.7

.. note:: The plugin supports only asyncio evenloop (not trio)

.. _installation:

Installation
=============

**Muffin-Mongo** should be installed using pip: ::

    pip install muffin-mongo

.. _usage:

Usage
=====

Setup the plugin and connect it into your app:

.. code-block:: python

    from muffin import Application
    from muffin_mongo import Plugin as Mongo

    # Create Muffin Application
    app = Application('example')

    # Initialize the plugin
    # As alternative: db = DB(app, **options)
    mongo = Mongo(db_url='mongodb://localhost:27017', database='db_name')
    mongo.setup(app)


That's it now you are able to use the plugin inside your views:

.. code-block:: python

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


Configuration options
----------------------

=========================== ======================================= =========================== 
Name                        Default value                           Desctiption
--------------------------- --------------------------------------- ---------------------------
**db_url**                  ``"mongodb://localhost:27017"``         A mongo connection URL
**database**                ``None``                                A database name (optional)
=========================== ======================================= =========================== 

You are able to provide the options when you are initiliazing the plugin:

.. code-block:: python

    mongo.setup(app, db_url='mongodb://localhost:27017')

Or setup it from ``Muffin.Application`` configuration using the ``MONGO_`` prefix:

.. code-block:: python

   MONGO_DB_URL = 'mongodb://localhost:27017'

``Muffin.Application`` configuration options are case insensitive

.. _bugtracker:

Bug tracker
===========

If you have any suggestions, bug reports or
annoyances please report them to the issue tracker
at https://github.com/klen/muffin-mongo/issues

.. _contributing:

Contributing
============

Development of Muffin-Mongo happens at: https://github.com/klen/muffin-mongo


Contributors
=============

* klen_ (Kirill Klenov)

.. _license:

License
========

Licensed under a `MIT license`_.

.. _links:


.. _klen: https://github.com/klen
.. _Muffin: https://github.com/klen/muffin
.. _MIT license: http://opensource.org/licenses/MIT
