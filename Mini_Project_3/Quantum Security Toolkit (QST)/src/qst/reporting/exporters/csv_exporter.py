"""CSV Exporter and CSVFlattener implementations.

References:
    Docs/EXPORT_SPEC.md §2
    Docs/07_SYSTEM_ARCHITECTURE.md §11
"""

import csv
import os
from typing import Any, Optional

from qst.exceptions.export import ExportError
from qst.exceptions.validation import ValidationError


class CSVFlattener:
    """Flattens nested dictionary representations into relational table records."""

    def flatten(
        self,
        data: dict[str, Any],
        metadata: Optional[dict[str, Any]] = None,
    ) -> list[dict[str, Any]]:
        """Convert nested dictionary tree into a list of flat row dictionaries.

        Args:
            data: Serialized data tree.
            metadata: Global metadata fields to inject.

        Returns:
            A list of flat dictionaries (one for each row).
        """
        # Check if data is ParameterSweepResult
        if "experiments" in data:
            return self._flatten_parameter_sweep(data, metadata)
        # Check if data is ExperimentResult
        elif "simulations" in data:
            return self._flatten_experiment(data, metadata)
        # Single SimulationResult
        else:
            return self._flatten_simulation(data, metadata)

    # 1-indexed indentation fixes
    def _flatten_simulation(
        self,
        sim_data: dict[str, Any],
        metadata: Optional[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        flat_sim = self._flatten_dict(sim_data)
        if metadata:
            flat_sim = {**metadata, **flat_sim}
        return [flat_sim]

    def _flatten_experiment(
        self,
        exp_data: dict[str, Any],
        metadata: Optional[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        sims = exp_data.get("simulations", [])
        global_keys = {k: v for k, v in exp_data.items() if k != "simulations"}
        flat_global = self._flatten_dict(global_keys, prefix="experiment")

        rows = []
        for sim in sims:
            flat_sim = self._flatten_dict(sim)
            merged = {**flat_global, **flat_sim}
            if metadata:
                merged = {**metadata, **merged}
            rows.append(merged)
        return rows

    def _flatten_parameter_sweep(
        self,
        sweep_data: dict[str, Any],
        metadata: Optional[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        exps = sweep_data.get("experiments", [])
        global_keys = {k: v for k, v in sweep_data.items() if k != "experiments"}
        flat_global = self._flatten_dict(global_keys, prefix="sweep")

        rows = []
        for exp in exps:
            exp_rows = self._flatten_experiment(exp, metadata=None)
            for exp_row in exp_rows:
                merged = {**flat_global, **exp_row}
                if metadata:
                    merged = {**metadata, **merged}
                rows.append(merged)
        return rows

    def _flatten_dict(
        self,
        d: dict[str, Any],
        prefix: str = "",
    ) -> dict[str, Any]:
        items: dict[str, Any] = {}
        for k, v in d.items():
            new_key = f"{prefix}_{k}" if prefix else k
            if isinstance(v, dict):
                items.update(self._flatten_dict(v, new_key))
            elif isinstance(v, (list, tuple)):
                items[new_key] = ",".join(map(str, v)) if v else ""
            elif v is None:
                items[new_key] = ""
            else:
                items[new_key] = v
        return items


class CSVExporter:
    """Exporter for saving normalized representations to tabular CSV format."""

    def __init__(self, overwrite_protection: bool = True) -> None:
        """Initialize CSVExporter.

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
        """Flatten and export data to a CSV file.

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
                f"CSVExporter only supports dictionary inputs, got {type(data)}",
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

        # Flatten records
        flattener = CSVFlattener()
        rows = flattener.flatten(data, metadata)

        headers = list(rows[0].keys()) if rows else []

        # Write to file
        try:
            with open(filepath, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=headers)
                writer.writeheader()
                writer.writerows(rows)
        except (OSError, PermissionError) as e:
            raise ExportError(
                f"Failed to write to file {filepath}: {str(e)}",
                code="QST-EXP-001",
            )
