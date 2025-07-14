import pytest
from uuid import uuid4

from app.schemas.article import Action
from app.tests.helpers import build_payload


ACTION_ID_KEY = {
    Action.CREATE:     "entityId",
    Action.PUBLISH:    "entityId",
    Action.GARBAGE:    "entityIds",
    Action.ARCHIVE:    "entityIds",
    Action.RESTORE:    "entityIds",
    Action.UNARCHIVE:  "entityIds",
}


@pytest.mark.anyio
@pytest.mark.parametrize("action", list(ACTION_ID_KEY))
async def test_webhook_accepts_all_article_events(action, async_client):
    """
    FastAPI route must return 2xx for every valid Teamly *article* event.
    """
    ids_key = ACTION_ID_KEY[action]
    ids_val = [str(uuid4()), str(uuid4())] if ids_key == "entityIds" else str(uuid4())

    resp = await async_client.post(
        "/v1/webhook",
        json=build_payload(action, ids_key, ids_val),
        timeout=1,          # SLA guard – fail fast if handler hangs
    )
    assert resp.status_code == 204


@pytest.mark.anyio
async def test_webhook_rejects_unknown_action(async_client):
    resp = await async_client.post(
        "/v1/webhook",
        json=build_payload("foo", "entityId", str(uuid4())),  # type: ignore[arg-type]
    )
    assert resp.status_code in {400, 422}


@pytest.mark.anyio
async def test_webhook_bad_schema_returns_422(async_client):
    resp = await async_client.post("/v1/webhook", json={"foo": "bar"})
    assert resp.status_code == 422
