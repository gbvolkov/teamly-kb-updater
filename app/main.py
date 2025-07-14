"""app/main.py

FastAPI application entry‑point for the Teamly **article‑webhook**
listener.

Run locally with:
    uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
"""
from __future__ import annotations

import logging
from contextlib import asynccontextmanager
from typing import cast

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.routes import router as v1_router
from app.core.logging import LogLevel, configure_logging
from app.core.config import get_settings

# ───────────────────────────────────────────
# Configuration & logging
# ───────────────────────────────────────────
settings = get_settings()
configure_logging(level=cast(LogLevel, settings.log_level.upper()))

# ───────────────────────────────────────────
# Lifespan hooks (startup/shutdown)
# ───────────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.getLogger(__name__).info("🚀 Webhook service starting")
    yield
    logging.getLogger(__name__).info("🛑 Webhook service shutting down")


app = FastAPI(
    title="Teamly Article Webhook",
    version="1.0.0",
    lifespan=lifespan,
)

if origins := getattr(settings, "allowed_origins", []):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_methods=["POST"],
        allow_headers=["*"],
    )

# ───────────────────────────────────────────
# Routes
# ───────────────────────────────────────────
app.include_router(v1_router)
# Ensure @register decorators run so the dispatcher registry is populated.
from app.handlers import article