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

- python >= 3.11
- motor (MongoDB driver)

.. note::

   The plugin supports only the asyncio event loop (not trio or curio).
   The plugin is a thin wrapper around `motor`_, and motor's asyncio driver is
   built directly on ``asyncio``: it looks up the running loop with
   ``asyncio.get_event_loop()`` and returns ``asyncio.Future`` objects. Any
   request made from a trio or curio task therefore fails with
   ``RuntimeError: There is no current event loop in thread 'MainThread'``.
   There is nothing to configure here -- the limitation comes from the
   database driver, not from Muffin. The plugin's own tests pin asyncio with
   an ``aiolib`` fixture for the same reason.

.. note::

   Motor 3.7 declares support up to Python 3.13 and is in maintenance mode
   (its author recommends moving to the ``pymongo`` async API). The plugin's
   test suite passes on Python 3.14 and 3.15 as well, but those versions are
   outside motor's own support range.

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


Public API
----------

The plugin exposes three things:

**client** (property)
    The underlying ``motor.motor_asyncio.AsyncIOMotorClient`` instance. It is
    created in ``setup()``, so reading the property before the plugin is bound
    to an application fails with ``AssertionError: Please setup plugin with an
    application.``

**__getattr__** (proxying)
    Every other attribute is proxied to motor: to the client itself, or to the
    database named by the ``database`` option when it is set. This is what
    makes the plugin feel transparent:

    .. code-block:: python

        # database='db_name' is set:
        mongo.items                 # AsyncIOMotorCollection('items' in 'db_name')
        mongo.items.find_one({})    # a collection method

        # database is not set (None):
        mongo.items                 # AsyncIOMotorDatabase('items')
        mongo.list_database_names() # a client method

    With ``database`` set the proxy points at the database, so client level
    methods (``list_database_names()``, ``drop_database()``, ``start_session()``,
    ...) are not reachable through the plugin -- use ``mongo.client`` for them.
    The same assertion as for ``client`` applies before ``setup()``.

**startup / shutdown** are *not* overridden.
    Motor connects lazily: creating the client opens nothing, the first
    operation does. The plugin does not override the two hooks (muffin runs
    ``BasePlugin``'s no-op versions) and it never closes the client when the
    application stops. Closing it is your job, typically on application
    shutdown:

    .. code-block:: python

        @app.on_shutdown
        async def shutdown():
            mongo.client.close()  # note: close() is not a coroutine

    The client is still usable after the application's lifespan ends -- until
    ``close()`` is called, after which motor raises
    ``pymongo.errors.InvalidOperation: Cannot use MongoClient after close``.


Configuration options
----------------------

=========================== ======================================= ===========================
Name                        Default value                           Description
--------------------------- --------------------------------------- ---------------------------
**db_url**                  ``"mongodb://localhost:27017"``         A mongo connection URL
**database**                ``None``                                A database name (optional)
=========================== ======================================= ===========================

``db_url`` is passed to ``AsyncIOMotorClient`` as is, so any MongoDB
connection string (replica set, credentials, options) works.

``database`` selects what the plugin proxies to: with a name, attributes are
resolved on that database (``mongo.items`` is a collection); with the default
``None`` they are resolved on the client (``mongo.items`` is a database,
``mongo.list_database_names()`` is available).

Unknown options are ignored: the plugin only knows the keys above, and an
option that doesn't match one of them is dropped instead of raising.

You are able to provide the options when you are initializing the plugin:

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
.. _motor: https://github.com/mongodb/motor
.. _MIT license: http://opensource.org/licenses/MIT
