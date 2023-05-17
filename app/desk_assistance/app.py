from abc import abstractmethod, ABC
import asyncio

from app.desk_assistance.config import AppConfig
from app.desk_assistance.plugin import PluginsBearer, Plugin


class App(PluginsBearer["AppPlugin"]):
    def __init__(self, *, config: AppConfig | None = None):
        self._config = config or AppConfig()

    @property
    def config(self):
        return self._config

    @classmethod
    def create(cls, *, plugins: list[Plugin] | None, config: AppConfig):
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
    @abstractmethod
    async def on_app_run(self):
        ...
