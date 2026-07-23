"""Custom log formatters for QST.

Supports standard text formatting and structured JSON formatting.

References:
    Docs/30_OBSERVABILITY.md
"""

import json
import logging
from typing import Any


class StandardFormatter(logging.Formatter):
    """Clean, readable console log formatter."""

    def __init__(self) -> None:
        """Initialize the standard formatter with a clean log format."""
        fmt = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        super().__init__(fmt=fmt, datefmt="%Y-%m-%d %H:%M:%S")


class StructuredJSONFormatter(logging.Formatter):
    """Structured JSON formatter for machine-readable logging output."""

    def __init__(self) -> None:
        """Initialize structured formatter."""
        super().__init__()

    def format(self, record: logging.LogRecord) -> str:
        """Format log record as a single JSON line.

        Args:
            record: The logging LogRecord to format.

        Returns:
            A serialized JSON string representing the log record details.
        """
        log_data: dict[str, Any] = {
            "timestamp": self.formatTime(record, self.datefmt),
            "logger": record.name,
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "line": record.lineno,
        }
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_data)
