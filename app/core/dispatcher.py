# app/core/dispatcher.py
from typing import Any, Awaitable, Callable, Dict, Tuple, Union, TypeVar
from pydantic import BaseModel
import anyio
import inspect
import logging

log = logging.getLogger(__name__)

T = TypeVar("T", bound=BaseModel)
Payload = Union[BaseModel, Dict[str, Any]]

Handler = Callable[[Payload], Awaitable[None]]

_HANDLERS: Dict[Tuple[str, str], Handler] = {}


def register(entity: str, action: str) -> Callable[[Handler], Handler]:
    """
    Decorator: register `async def handler(payload)` for an (entity, action) key.
    The payload may be a Pydantic model **or** a plain dict.
    """
    def wrapper(func: Handler) -> Handler:
        _HANDLERS[(entity, action)] = func
        return func
    return wrapper


async def dispatch(payload: Payload) -> None:
    """
    Route the payload to its handler.

    * Accepts either a raw dict (old behaviour) or a Pydantic model.
    * If it’s a model we keep it **as-is** so handlers get type safety.
    """
    # Make a dict-view regardless of the original type
    data = payload.model_dump() if isinstance(payload, BaseModel) else payload

    try:
        key = (data["entityType"], data["action"])
        handler = _HANDLERS[key]
    except KeyError as exc:  # no such handler
        raise ValueError(f"Unhandled event type: {key}") from exc

    # Call the handler.  If it’s sync, run it in a worker thread.
    if inspect.iscoroutinefunction(handler):
        await handler(payload)          # async handler
    else:
        await anyio.to_thread.run_sync(handler, payload)  # sync handler
