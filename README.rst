Muffin-Mongo
############

.. _description:

Muffin-Mongo -- MongoDB support for Muffin framework.

.. _badges:

.. image:: http://img.shields.io/travis/klen/muffin-mongo.svg?style=flat-square
    :target: http://travis-ci.org/klen/muffin-mongo
    :alt: Build Status

.. image:: http://img.shields.io/pypi/v/muffin-mongo.svg?style=flat-square
    :target: https://pypi.python.org/pypi/muffin-mongo

.. image:: http://img.shields.io/pypi/dm/muffin-mongo.svg?style=flat-square
    :target: https://pypi.python.org/pypi/muffin-mongo

.. _contents:

.. contents::

.. _requirements:

Requirements
=============

- python >= 3.3

.. _installation:

Installation
=============

**Muffin-Mongo** should be installed using pip: ::

    pip install muffin-mongo

.. _usage:

Usage
=====

Add `muffin_mongo` to `PLUGINS` in your Muffin Application configuration.

Or install it manually like this: ::

    mongo = muffin_mongo.Plugin(**{'options': 'here'})

    app = muffin.Application('test')
    app.install(mongo)


Appllication configuration options
----------------------------------

``MONGO_HOST``       -- Connection IP address (127.0.0.1)
``MONGO_PORT``       -- Connection port (27017)
``MONGO_DB``         -- Connection database (None)
``MONGO_USERNAME``   -- Connection username (None)
``MONGO_PASSWORD``   -- Connection password (None)
``MONGO_POOL``       -- Connection pool size (1)

Queries
-------

::

    @app.register
    def view(request):
        foo = app.mongo.foo  # foo database
        test = foo.test      # test collection

        # fetch some documents
        docs = yield from test.find(limit=10)
        return list(docs)

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
=======

Licensed under a `MIT license`_.

.. _links:

If you wish to express your appreciation for the project, you are welcome to send
a postcard to: ::

    Kirill Klenov
    pos. Severny 8-3
    MO, Istra, 143500
    Russia


.. _klen: https://github.com/klen
.. _MIT license: http://opensource.org/licenses/MIT
