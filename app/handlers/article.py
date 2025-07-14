"""app/handlers/article.py

Business‑logic handlers for Teamly *article* webhook events.
The functions are registered with `app.core.dispatcher` via the
`@register` decorator so the dispatcher can invoke them by `(entityType,
action)`.

For now they only log; swap the log statement for real work (database
writes, message‑queue publishes, calls to other micro‑services, etc.) as
needed.
"""
from __future__ import annotations

import logging

from app.core.dispatcher import register
from app.schemas.article import Action, ArticleEvent

logger = logging.getLogger(__name__)

# ───────────────────────────────────────────
# CREATE
# ───────────────────────────────────────────


@register("article", Action.CREATE)
def create(event: ArticleEvent) -> None:  # noqa: D401  (simple verb name ok)
    """Handle *create* event for a single article."""
    logger.info("[webhook] article.create id=%s", getattr(event, "entityId", None))


# ───────────────────────────────────────────
# PUBLISH
# ───────────────────────────────────────────


@register("article", Action.PUBLISH)
def publish(event: ArticleEvent) -> None:
    """Handle *publish* event for a single article."""
    logger.info("[webhook] article.publish id=%s", getattr(event, "entityId", None))


# ───────────────────────────────────────────
# GARBAGE & ARCHIVE share the same handler
# ───────────────────────────────────────────


@register("article", Action.GARBAGE, Action.ARCHIVE)
def remove_or_archive(event: ArticleEvent) -> None:
    """Handle *garbage* or *archive* bulk‑status change."""
    logger.info("[webhook] article.%s ids=%s", event.action, getattr(event, "entityIds", None))


# ───────────────────────────────────────────
# RESTORE
# ───────────────────────────────────────────


@register("article", Action.RESTORE)
def restore(event: ArticleEvent) -> None:
    """Handle *restore* bulk‑status change."""
    logger.info("[webhook] article.restore ids=%s", getattr(event, "entityIds", None))


# ───────────────────────────────────────────
# UNARCHIVE
# ───────────────────────────────────────────


@register("article", Action.UNARCHIVE)
def unarchive(event: ArticleEvent) -> None:
    """Handle *unarchive* bulk‑status change."""
    logger.info("[webhook] article.unarchive ids=%s", getattr(event, "entityIds", None))
