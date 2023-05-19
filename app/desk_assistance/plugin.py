import typing as t
from abc import ABC
from typing import Self
import contextlib

if t.TYPE_CHECKING:
    from desk_assistance.event import Event

PluginsBearerT = t.TypeVar(
    "PluginsBearerT", bound="PluginsBearer", covariant=True
)
PluginT = t.TypeVar("PluginT", bound="Plugin", covariant=True)


class PluginsBearer(
    t.Generic[PluginT], contextlib.AbstractAsyncContextManager
):
    def __init__(self):
        self._plugins: list[PluginT] = []
        self._context_stack: contextlib.AsyncExitStack | None = None

    @property
    def context_entered(self) -> bool:
        return self._context_stack is not None

    async def _establish_context(
        self, context_stack: contextlib.AsyncExitStack
    ) -> contextlib.AsyncExitStack:
        for plugin in self._plugins:
            await context_stack.enter_async_context(plugin)

        return context_stack

    async def __aenter__(self) -> Self:
        if self.context_entered:
            return self

        context_stack = contextlib.AsyncExitStack()
        async with context_stack:
            context_stack = await self._establish_context(context_stack)
            self._context_stack = context_stack.pop_all()

        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self._context_stack is None:
            return

        await self._context_stack.aclose()
        self._context_stack = None

    def register(self, plugin: PluginT):
        # TODO: Choose politic for "plugin already bound to something"
        #  - Option 1 - Raise only when plugin bound to another plugin bearer
        #  - Option 2 - Raise when plugin bound to any plugin bearer
        if plugin.bound_bearer is not None:
            # TODO: When chose Option 2 in above TODO remove below condition
            #  and return
            if plugin.bound_bearer is self:
                return
            raise ...

        self._plugins.append(plugin)
        plugin.bound_bearer = self

    def unregister(self, plugin: PluginT):
        if plugin.bound_bearer is not self:
            # TODO: Consider raising exception (cannot unregister plugin non
            #  registered at this bearer). This decision should be consistent
            #  with politic chosen at `PluginBearer.register` method
            return
        self._plugins.remove(plugin)
        plugin.bound_bearer = None

    async def trigger(self, event: "Event"):
        for plugin in self._plugins:
            await plugin.trigger(event)


class Plugin(
    t.Generic[PluginsBearerT], ABC, contextlib.AbstractAsyncContextManager
):
    def __init__(self):
        self._bound_bearer: PluginsBearerT | None = None

    @property
    def bound_bearer(self) -> PluginsBearerT:
        return self._bound_bearer

    def register_at(self, bearer: PluginsBearerT) -> None:
        bearer.register(self)

    def unregister(self) -> None:
        self.bound_bearer.unregister(self)

    async def trigger(self, event: "Event"):
        await event.trigger_at(self)
