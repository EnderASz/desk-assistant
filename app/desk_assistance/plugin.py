class Plugin:
    def __init__(self):
        self._bound_bearer: "PluginsBearer" | None = None

    @property
    def bound_bearer(self) -> "PluginsBearer":
        return self._bound_bearer

    def register_at(self, bearer: "PluginsBearer") -> None:
        bearer.register(self)

    def unregister(self) -> None:
        self.bound_bearer.unregister(self)


class PluginsBearer:
    def __init__(self):
        self._plugins: list[Plugin] = []

    def register(self, plugin: Plugin):
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

    def unregister(self, plugin: Plugin):
        if plugin.bound_bearer is not self:
            # TODO: Consider raising exception (cannot unregister plugin non
            #  registered at this bearer). This decision should be consistent
            #  with politic chosen at `PluginBearer.register` method
            return
        self._plugins.remove(plugin)
        plugin.bound_bearer = None
