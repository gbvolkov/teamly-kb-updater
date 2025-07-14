"""app/core/logging.py

Minimal structured logging configuration for the webhook service.

`configure_logging(level)` must be imported and executed early (from
`app.main`) so the root logger is set up exactly once.
"""
from __future__ import annotations

import logging
import sys
from typing import Literal

LogLevel = Literal["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG"]


def configure_logging(level: LogLevel = "INFO") -> None:
    """Configure root logger with sane defaults.

    Parameters
    ----------
    level:
        Textual log level (case‑insensitive). Defaults to "INFO".
    """
    numeric_level = logging.getLevelName(level.upper())  # type: ignore[arg-type]
    logging.basicConfig(
        level=numeric_level,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
        stream=sys.stdout,
        datefmt="%Y-%m-%dT%H:%M:%S%z",
    )

    # Reduce noise from uvicorn's access logger (optional)
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
