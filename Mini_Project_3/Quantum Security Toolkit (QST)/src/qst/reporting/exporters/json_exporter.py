"""JSON Exporter implementation.

References:
    Docs/EXPORT_SPEC.md §1
    Docs/07_SYSTEM_ARCHITECTURE.md §11
"""

import json
import os
from typing import Any, Optional

from qst.exceptions.export import ExportError
from qst.exceptions.validation import ValidationError


class JSONExporter:
    """Exporter for saving normalized representations to deterministic JSON format."""

    def __init__(self, overwrite_protection: bool = True) -> None:
        """Initialize JSONExporter.

        Args:
            overwrite_protection: If True, blocks overwriting existing files.
        """
        self.overwrite_protection = overwrite_protection

    def export(
        self,
        filepath: str,
        data: dict[str, Any],
        metadata: dict[str, Any],
    ) -> None:
        """Serialize and export data to a JSON file.

        Args:
            filepath: Path to the target file.
            data: Normalized dictionary containing domain metrics.
            metadata: Structured dictionary of export metadata attributes.

        Raises:
            ValidationError: For invalid filenames, existing files, or unsupported types.
            ExportError: For file-system or OS write permission errors.
        """
        if not filepath:
            raise ValidationError("Filepath must not be empty.", code="QST-VAL-401")

        if not isinstance(data, dict):
            raise ValidationError(
                f"JSONExporter only supports dictionary inputs, got {type(data)}",
                code="QST-VAL-404",
            )

        # Overwrite protection check
        if self.overwrite_protection and os.path.exists(filepath):
            raise ValidationError(
                f"File already exists at {filepath} and overwrite protection is active.",
                code="QST-VAL-402",
            )

        # Directory validation & creation
        parent_dir = os.path.dirname(filepath)
        if parent_dir:
            try:
                os.makedirs(parent_dir, exist_ok=True)
            except OSError as e:
                raise ExportError(
                    f"Failed to create directory {parent_dir}: {str(e)}",
                    code="QST-EXP-401",
                )

        # Verify parent directory is a directory
        if parent_dir and not os.path.isdir(parent_dir):
            raise ValidationError(
                f"Parent path {parent_dir} is not a directory.",
                code="QST-VAL-403",
            )

        # Wrap content inside metadata envelope
        payload = {
            "schema_version": metadata.get("schema_version", "1.0.0"),
            "metadata": metadata,
            "data": data,
        }

        # Write to file
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(payload, f, indent=4, sort_keys=True)
        except (OSError, PermissionError) as e:
            raise ExportError(
                f"Failed to write to file {filepath}: {str(e)}",
                code="QST-EXP-001",
            )
