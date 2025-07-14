"""app/core/config.py

Environment‑driven configuration using Pydantic Settings (v2).
"""
from __future__ import annotations

from functools import lru_cache
from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # HTTP server
    host: str = "0.0.0.0"
    port: int = 8000

    # Logging
    log_level: str = "INFO"

    # CORS
    allowed_origins: List[str] = []

    model_config = SettingsConfigDict(env_prefix="TEAMLY_", env_file=".env", extra="ignore")


@lru_cache(1)
def get_settings() -> Settings:  # pragma: no cover
    """Return a cached Settings instance."""
    return Settings()