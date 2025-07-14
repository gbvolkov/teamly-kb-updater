"""
Utility functions shared by multiple test modules.
(Helpers live here so individual tests never import one another.)
"""
from uuid import uuid4
from app.schemas.article import Action


def build_payload(action: Action | str, ids_key: str, ids_val):
    """
    Produce a minimal Teamly **article** webhook body.

    Parameters
    ----------
    action   Teamly article action  (create, publish, garbage, …)
    ids_key  'entityId' or 'entityIds'
    ids_val  uuid str  *or*  list[str]
    """
    return {
        "entityType": "article",
        "action": action,
        ids_key: ids_val,
        "content": {"containerId": str(uuid4())},
    }
