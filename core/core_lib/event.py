import typing as t
from enum import Enum

from pydantic import BaseModel

from core_lib.exc import EventNotSupported


class EventType(str, Enum):
    ...


EventHandlerT = t.TypeVar("EventHandlerT", covariant=True)


class Event(BaseModel, t.Generic[EventHandlerT]):
    EVENT_TYPE: EventType

    async def trigger_at(self, handler: EventHandlerT):
        try:
            handler_method = getattr(handler, f"on_{self.EVENT_TYPE.lower()}")
        except AttributeError:
            # TODO: Add missing exception parameters
            raise EventNotSupported(
                f"{self.__class__} event is not supported by: {handler}"
            )

        await handler_method(handler, self)
