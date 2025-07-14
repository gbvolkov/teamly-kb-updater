"""app/core/dispatcher.py

Central routing for Teamly webhook events.

* Validates incoming payloads (dict) against the union `ArticleEvent`
  using `pydantic.TypeAdapter` (works with `typing.Union`).
* Maps the `(entityType, action)` pair to a handler previously registered
  via the `@register` decorator.
* Executes the handler whether it is `async def` or plain `def`,
  off‑loading sync functions to a worker thread so the event‑loop
  remains unblocked.

The module is **MyPy‑strict clean** with Python ≥ 3.12.
"""
from __future__ import annotations

#import asyncio
import anyio 
import inspect
import logging
from typing import Any, Awaitable, Callable, Dict, Tuple

from pydantic import ValidationError, TypeAdapter

from app.schemas.article import Action, ArticleEvent

logger = logging.getLogger(__name__)

# ────────────────────────────────────────────
# Type aliases
# ────────────────────────────────────────────
Handler = Callable[[ArticleEvent], Awaitable[None] | None]
Key = Tuple[str, Action]

# Registry mapping (entity_type, action) → handler
_registry: Dict[Key, Handler] = {}

# ────────────────────────────────────────────
# Decorator for registration
# ────────────────────────────────────────────

def register(entity_type: str, *actions: Action) -> Callable[[Handler], Handler]:
    """Decorator to bind one or more *actions* for an *entity* to a handler."""

    if not actions:
        raise ValueError("@register requires at least one Action argument")

    def decorator(func: Handler) -> Handler:
        for action in actions:
            key: Key = (entity_type, action)
            if key in _registry:
                raise ValueError(
                    f"Handler already registered for {key}: {_registry[key]}"
                )
            _registry[key] = func
            logger.debug("Registered handler %s → %s", key, func.__qualname__)
        return func

    return decorator


# ────────────────────────────────────────────
# Public dispatch function
# ────────────────────────────────────────────

async def dispatch(event_dict: dict[str, Any], *, registry=_registry) -> None:
    """
    Validate **event_dict** against the Article schema and run the matching
    handler.  Raises:
      * pydantic.ValidationError – bad schema  → HTTP 422
      * ValueError               – unknown action → HTTP 400
    """
    # 1) schema validation
    event: ArticleEvent = TypeAdapter(ArticleEvent).validate_python(event_dict)  # type: ignore[assignment]

    # 2) handler lookup
    try:
        handler = registry[(event.entityType, event.action)]
    except KeyError as exc:
        raise ValueError(f"No handler registered for {(event.entityType, event.action)!r}") from exc

    # 3) run it (async-aware)
    if inspect.iscoroutinefunction(handler):
        await handler(event)
    else:
        #await asyncio.to_thread(handler, event)
        await anyio.to_thread.run_sync(handler, event)