# app/schemas/article.py
from enum import Enum
from typing import List, Literal, Union
from uuid import UUID

from pydantic import BaseModel, Field


# ───────────────────────────────────────────
# 1. Enum for all 6 article-specific actions
# ───────────────────────────────────────────
class Action(str, Enum):
    CREATE = "create"
    PUBLISH = "publish"
    GARBAGE = "garbage"
    RESTORE = "restore"
    ARCHIVE = "archive"
    UNARCHIVE = "unarchive"


# ───────────────────────────────────────────
# 2. Common envelope fields for *any* event
# ───────────────────────────────────────────
class _Envelope(BaseModel):
    """Fields that come *outside* the `content` block."""

    entityType: Literal["article"]  # always “article” for this module
    action: Action


# ───────────────────────────────────────────
# 3. `content` block used by *all* article
#    events (just one field according to doc)
# ───────────────────────────────────────────
class _ArticleContent(BaseModel):
    containerId: UUID = Field(
        ...,
        description="UUID of the space that contains the article",
    )  # :contentReference[oaicite:0]{index=0}


# ───────────────────────────────────────────
# 4. Single-entity events:  create / publish
# ───────────────────────────────────────────
class _SingleArticleEvent(_Envelope):
    entityId: UUID  # single target article


class ArticleCreateEvent(_SingleArticleEvent):
    action: Literal[Action.CREATE]
    content: _ArticleContent  # only `containerId` is present :contentReference[oaicite:1]{index=1}


class ArticlePublishEvent(_SingleArticleEvent):
    action: Literal[Action.PUBLISH]
    content: _ArticleContent  # same payload spec as “create” today


# ───────────────────────────────────────────
# 5. Bulk events: garbage / restore / archive /
#    unarchive — note `entityIds` instead of
#    `entityId` (array of UUIDs) :contentReference[oaicite:2]{index=2}
# ───────────────────────────────────────────
class _BulkArticleEvent(_Envelope):
    entityIds: List[UUID]


class ArticleStatusChangeEvent(_BulkArticleEvent):
    action: Literal[
        Action.GARBAGE,
        Action.RESTORE,
        Action.ARCHIVE,
        Action.UNARCHIVE,
    ]
    content: _ArticleContent


# ───────────────────────────────────────────
# 6. Convenience union for the dispatcher
# ───────────────────────────────────────────
ArticleEvent = Union[
    ArticleCreateEvent,
    ArticlePublishEvent,
    ArticleStatusChangeEvent,
]
