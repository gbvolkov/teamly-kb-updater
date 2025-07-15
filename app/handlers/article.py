# app/handlers/article.py
import logging
from app.core import dispatcher
from app.schemas.article import (
    ArticleCreateEvent,
    ArticlePublishEvent,
    ArticleStatusChangeEvent,
)

logger = logging.getLogger(__name__)     # ← renamed


@dispatcher.register("article", "create")
async def create(event: ArticleCreateEvent) -> None:
    logger.info("[webhook] article.create id=%s", event.entityId)


@dispatcher.register("article", "publish")
async def publish(event: ArticlePublishEvent) -> None:
    logger.info(
        "[webhook] article.publish id=%s space=%s",
        event.entityId,
        event.content.containerId,
    )


@dispatcher.register("article", "garbage")
async def garbage(event: ArticleStatusChangeEvent) -> None:
    logger.info(
        "[webhook] article.garbage ids=%s space=%s",
        event.entityIds,
        event.content.containerId,
    )
