"""MonfoDB support for Muffin Framework."""

import typing as t

from muffin import Application
from motor import motor_asyncio as motor
from muffin.plugin import BasePlugin

__version__ = "0.3.2"
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
        self.__client__ = None
        super().__init__(*args, **kwargs)

    def setup(self, app: Application, **options):
        """Initialize a mongo client."""
        super().setup(app, **options)
        self.__client__ = motor.AsyncIOMotorClient(self.cfg.db_url)

    def __getattr__(self, name) -> t.Any:
        """Proxy methods to the motor client."""
        proxy = self.__client__
        if self.cfg.database:
            proxy = self.__client__[self.cfg.database]
        return getattr(proxy, name)

    @property
    def client(self):
        """Proxy the client."""
        assert self.__client__, 'Please setup plugin with an application.'
        return self.__client__
