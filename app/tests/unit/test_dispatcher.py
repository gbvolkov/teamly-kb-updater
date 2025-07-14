import pytest
from unittest.mock import AsyncMock
from uuid import uuid4

from app.core import dispatcher
from app.schemas.article import Action
from app.tests.helpers import build_payload


ACTION_HANDLER_MAP = {
    Action.CREATE:     "create",
    Action.PUBLISH:    "publish",
    Action.GARBAGE:    "remove_or_archive",
    Action.ARCHIVE:    "remove_or_archive",
    Action.RESTORE:    "restore",
    Action.UNARCHIVE:  "unarchive",
}

BULK = {Action.GARBAGE, Action.ARCHIVE, Action.RESTORE, Action.UNARCHIVE}


@pytest.mark.anyio
@pytest.mark.parametrize("action, handler_attr", ACTION_HANDLER_MAP.items())
async def test_dispatcher_invokes_correct_handler_via_injection(action, handler_attr):
    ids_key = "entityIds" if action in BULK else "entityId"
    ids_val = [str(uuid4()), str(uuid4())] if ids_key == "entityIds" else str(uuid4())

    mock = AsyncMock()
    custom_registry = {("article", action): mock}

    await dispatcher.dispatch(
        build_payload(action, ids_key, ids_val),
        registry=custom_registry,          # ← inject mock table
    )

    mock.assert_awaited_once()


@pytest.mark.anyio
async def test_dispatcher_unknown_action_raises():
    with pytest.raises(ValueError):
        await dispatcher.dispatch(
            build_payload("foo", "entityId", str(uuid4())),
            registry={},                    # empty table forces KeyError branch
        )
