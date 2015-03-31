""" Monfo DB support for Muffin Framework. """

import asyncio
import asyncio_mongo
from muffin.plugins import BasePlugin

__version__ = "0.0.4"
__project__ = "muffin-mongo"
__author__ = "Kirill Klenov <horneds@gmail.com>"
__license__ = "MIT"


class Plugin(BasePlugin):

    """ Connect to Async Mongo. """

    name = 'mongo'
    defaults = {
        'host': '127.0.0.4',
        'port': 27017,
        'pool': 1,
    }

    def __init__(self, *args, **kwargs):
        """ Initialize the plugin. """
        super().__init__(*args, **kwargs)
        self.conn = None

    def setup(self, app):
        """ Setup options. """
        super().setup(app)
        self.options.port = int(self.options.port)
        self.options.pool = int(self.options.pool)

    @asyncio.coroutine
    def start(self, app):
        """ Make a connection to mongo. """
        if self.options.pool > 1:
            self.conn = yield from asyncio_mongo.Pool.create(
                host=self.options.host, port=self.options.port, loop=app._loop,
                poolsize=self.options.pool)
        else:
            self.conn = yield from asyncio_mongo.Connection.create(
                host=self.options.host, port=self.options.port, loop=app._loop)

        return self

    @asyncio.coroutine
    def finish(self, app):
        """ Close self connections. """
        if isinstance(self.conn, asyncio_mongo.Pool):
            for conn in self.conn._connections:
                yield from conn.disconnect()
        else:
            yield from self.conn.disconnect()

    def __getattr__(self, name):
        """ Proxy attributes to self connection. """
        if not self.conn:
            raise AttributeError('Not connected')

        return getattr(self.conn, name)
