import typing as t
from enum import Enum
from typing import Self
from abc import abstractmethod, ABC
import asyncio
import contextlib

from desk_assistance.config import AppConfig
from desk_assistance.plugin import PluginsBearer, Plugin


class App(PluginsBearer["AppPlugin"], contextlib.AbstractAsyncContextManager):
    def __init__(self, *, config: AppConfig | None = None):
        super().__init__()

        self._config: AppConfig = config or AppConfig()

    @property
    def config(self) -> AppConfig:
        return self._config

    @classmethod
    def create(
        cls, *, plugins: list[Plugin] | None, config: AppConfig
    ) -> Self:
        app = cls(config=config)
        for plugin in plugins or []:
            app.register(plugin)

        return app

    async def _run(self):
        ...

    def run(self):
        # TODO: Raise exception if this or any other app instance is currently
        #  running. Also consider if this check should be here or at `App._run`
        #  method.

        asyncio.run(self._run())


class AppPlugin(Plugin[App], ABC):
    """
    Plugin applicable to App instance
    """

    @abstractmethod
    async def on_app_run(self):
        ...
