import asyncio

from app.desk_assistance.plugin import PluginsBearer


class App(PluginsBearer):
    @classmethod
    def create(cls):
        return cls()

    async def _run(self):
        ...

    def run(self):
        # TODO: Raise exception if this or any other app instance is currently
        #  running. Also consider if this check should be here or at `App._run`
        #  method.

        asyncio.run(self._run())
