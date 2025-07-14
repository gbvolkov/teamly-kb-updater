"""v1 HTTP routes for the Teamly webhook listener."""
from __future__ import annotations

from fastapi import APIRouter, HTTPException, Request, status
from pydantic import ValidationError

from app.core.dispatcher import dispatch

router = APIRouter(prefix="/v1", tags=["webhook"])


@router.post("/webhook", status_code=status.HTTP_204_NO_CONTENT)
async def handle_webhook(payload: dict):
    try:
        await dispatch(payload)

    # 422 – schema/body didn’t validate
    except ValidationError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Invalid webhook payload",
        ) from exc

    # 400 – the dispatcher accepted the shape but had no mapping
    # (covers both ValueError and KeyError depending on dispatcher version)
    except (ValueError, KeyError) as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unhandled event type: {exc}",
        ) from exc
