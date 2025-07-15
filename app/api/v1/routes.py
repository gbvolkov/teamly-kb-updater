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
    payload: Annotated[
        ArticleEvent,                     # Union of the three concrete models
        Body(                             # tell FastAPI how to discriminate
            discriminator="action"        # ← field present in every variant
        ),
    ]
):
    # If you still want to reuse your dispatcher, pass the *model* or dict:
    await dispatch(payload.model_dump())   # or adapt dispatcher to take the model
