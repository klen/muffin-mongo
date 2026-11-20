"""MongoDB support for Muffin Framework."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, ClassVar, Mapping

from motor import motor_asyncio as motor
from muffin.plugins import BasePlugin

if TYPE_CHECKING:
    from muffin import Application


class Plugin(BasePlugin):
    """Manage Motor Client."""

    name = "mongo"
    defaults: ClassVar[Mapping[str, Any]] = {
        "db_url": "mongodb://localhost:27017",
        "database": None,
    }

    def __init__(self, app: Application | None = None, **options: Any) -> None:
        """Initialize the plugin."""
        self.__client__: motor.AsyncIOMotorClient[Any] | None = None
        super().__init__(app, **options)

    def setup(self, app: Application, *, name: str | None = None, **options: Any) -> bool:
        """Initialize a mongo client."""
        enabled = super().setup(app, name=name, **options)
        self.__client__ = motor.AsyncIOMotorClient(self.cfg.db_url)
        return enabled

    def __getattr__(self, name: str) -> Any:
        """Proxy methods to the motor client."""
        if name in ("startup", "shutdown", "middleware"):
            return object.__getattribute__(self, name)

        assert self.__client__, "Please setup plugin with an application."
        proxy: motor.AsyncIOMotorClient[Any] | motor.AsyncIOMotorDatabase[Any] = self.__client__
        if self.cfg.database:
            proxy = self.__client__[self.cfg.database]
        return getattr(proxy, name)

    @property
    def client(self) -> motor.AsyncIOMotorClient[Any]:
        """Proxy the client."""
        assert self.__client__, "Please setup plugin with an application."
        return self.__client__
