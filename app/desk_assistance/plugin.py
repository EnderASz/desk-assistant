class Plugin:
    ...


class PluginsBearer:
    def __init__(self):
        self._plugins: list[Plugin] = []
