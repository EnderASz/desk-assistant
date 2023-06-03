import typing as t
from abc import ABC
import contextlib

from core_lib import exc
from core_lib.context import AbstractAsyncContextStackManager

if t.TYPE_CHECKING:
    from core_lib.event import Event


PluginsBearerT = t.TypeVar(
    "PluginsBearerT", bound="PluginsBearer", covariant=True
)
PluginT = t.TypeVar("PluginT", bound="Plugin", covariant=True)


class PluginsBearer(t.Generic[PluginT], AbstractAsyncContextStackManager):
    def __init__(self):
        super().__init__()
        self._plugins: list[PluginT] = []

    @property
    def plugins(self) -> tuple[PluginT]:
        return tuple(self._plugins)

    async def _establish_context(
        self, context_stack: contextlib.AsyncExitStack
    ) -> contextlib.AsyncExitStack:
        for plugin in self.plugins:
            await context_stack.enter_async_context(plugin)

        return context_stack

    def register(self, plugin: PluginT) -> None:
        """
        Registers and bounds plugin.

        :param plugin: Plugin instance
        """
        if self.context_entered:
            raise exc.ContextAlreadyEntered(
                "Cannot register plugin to already context entered bearer"
            )

        if plugin.bearer is not None:
            raise exc.PluginAlreadyRegistered(
                "Cannot register plugin that is already registered at any "
                "plugin plugin bearer"
            )

        self._plugins.append(plugin)
        plugin._bearer = self

    def unregister(self, plugin: PluginT) -> None:
        """
        Unregisters and unbound plugin..
        :param plugin:
        """
        if self.context_entered:
            raise exc.ContextAlreadyEntered(
                "Cannot unregister plugin from already context entered bearer"
            )
        if plugin.bound_bearer is not self:
            raise exc.PluginNotRegistered(
                f"{self} cannot unregister non-registered plugin."
            )
        self._plugins.remove(plugin)
        plugin._bearer = None

    async def trigger(self, event: "Event"):
        for plugin in self.plugins:
            await event.trigger_at(plugin)


class Plugin(t.Generic[PluginsBearerT], AbstractAsyncContextStackManager, ABC):
    def __init__(self):
        super().__init__()
        self._bearer: PluginsBearerT | None = None

    @property
    def bearer(self) -> PluginsBearerT:
        return self._bearer
