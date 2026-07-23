"""Central logging factory for QST.

Provides uniform logging configuration across all package modules.

References:
    Docs/30_OBSERVABILITY.md
"""

import logging
from pathlib import Path
from typing import Optional

from qst.logging.handlers import get_console_handler, get_file_handler


def get_logger(
    name: str,
    level: int = logging.INFO,
    structured: bool = False,
    log_file: Optional[Path] = None,
) -> logging.Logger:
    """Central factory function to retrieve configured logger.

    Args:
        name: Name of the logger, typically __name__.
        level: Minimum severity level to log.
        structured: If True, outputs logs in structured JSON format.
        log_file: Optional path to write log statements.

    Returns:
        The configured logger instance.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Avoid duplicate handler registration
    if not logger.handlers:
        logger.addHandler(get_console_handler(structured=structured))
        if log_file:
            file_h = get_file_handler(log_file, structured=structured)
            if file_h:
                logger.addHandler(file_h)

    return logger
