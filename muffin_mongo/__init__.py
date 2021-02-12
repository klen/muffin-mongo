"""MonfoDB support for Muffin Framework."""

import typing as t

from motor import motor_asyncio as motor
from muffin.plugin import BasePlugin

__version__ = "0.1.0"
__project__ = "muffin-mongo"
__author__ = "Kirill Klenov <horneds@gmail.com>"
__license__ = "MIT"


class Plugin(BasePlugin):

    """Manage Motor Client."""

    name = 'mongo'
    defaults = {
        'db_url': 'mongodb://localhost:27017',
        'database': None,
    }

    def __init__(self, *args, **kwargs):
        """Initialize the plugin."""
        super().__init__(*args, **kwargs)
        self.__client__ = None

    def __getattr__(self, name) -> t.Any:
        """Proxy methods to the motor client."""
        proxy = self.__client__
        if self.cfg.database:
            proxy = self.__client__[self.cfg.database]
        return getattr(proxy, name)

    async def startup(self):
        """Make a connection to mongo."""
        self.__client__ = motor.AsyncIOMotorClient(self.cfg.db_url)

    @property
    def client(self):
        return self.__client__