"""MonfoDB support for Muffin Framework."""
from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar, Optional

from motor import motor_asyncio as motor
from muffin.plugins import BasePlugin

if TYPE_CHECKING:
    from muffin import Application


class Plugin(BasePlugin):

    """Manage Motor Client."""

    name = "mongo"
    defaults: ClassVar = {
        "db_url": "mongodb://localhost:27017",
        "database": None,
    }

    def __init__(self, *args, **kwargs):
        """Initialize the plugin."""
        self.__client__: Optional[motor.AsyncIOMotorClient] = None
        super().__init__(*args, **kwargs)

    def setup(self, app: Application, **options):
        """Initialize a mongo client."""
        super().setup(app, **options)
        self.__client__ = motor.AsyncIOMotorClient(self.cfg.db_url)

    def __getattr__(self, name):
        """Proxy methods to the motor client."""
        if name in ("startup", "shutdown", "middleware"):
            return object.__getattribute__(self, name)

        assert self.__client__, "Please setup plugin with an application."
        proxy = self.__client__
        if self.cfg.database:
            proxy = self.__client__[self.cfg.database]
        return getattr(proxy, name)

    @property
    def client(self):
        """Proxy the client."""
        assert self.__client__, "Please setup plugin with an application."
        return self.__client__
