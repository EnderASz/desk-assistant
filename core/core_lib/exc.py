import typing as t

if t.TYPE_CHECKING:
    from core_lib.event import Event, EventHandlerT


class EventNotSupported(NotImplementedError):
    # TODO: Do something with parameters and consider adding some more
    def __init__(self, msg: str, event: "Event", handler: "EventHandlerT"):
        super().__init__(msg)


class ContextAlreadyEntered(Exception):
    ...


class MissingContext(Exception):
    ...


class PluginNotRegistered(Exception):
    ...


class PluginAlreadyRegistered(Exception):
    ...
