from typing import Annotated
from fastapi import Body, APIRouter, status
from app.schemas.article import ArticleEvent   
from app.core.dispatcher import dispatch

router = APIRouter(prefix="/v1", tags=["webhook"])

@router.post(
    "/webhook",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def handle_webhook(
    payload: Annotated[ArticleEvent, Body(discriminator="action")]
):
    await dispatch(payload)        