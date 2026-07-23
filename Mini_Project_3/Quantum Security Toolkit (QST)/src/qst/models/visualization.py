"""VisualizationResult model for QST.

References:
    Docs/VISUALIZATION_SPEC.md §2, §6
"""

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class VisualizationResult:
    """Coordinate, styling, and text payload representing plotted data.

    Attributes:
        coordinates: List of (x, y) plot coordinates.
        title: Descriptive graph title.
        labels: Mapping of axis names to text representations.
        extra: Additional metadata or rendering config properties.
    """

    coordinates: list[tuple[float, float]]
    title: str
    labels: dict[str, str]
    extra: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class LineSeries:
    """Immutable dataset model representing a line graph series."""

    label: str
    x_values: tuple[float, ...]
    y_values: tuple[float, ...]

    def __post_init__(self) -> None:
        """Validate alignment of coordinates."""
        from qst.exceptions.validation import ValidationError

        if len(self.x_values) != len(self.y_values):
            raise ValidationError(
                f"LineSeries x_values size ({len(self.x_values)}) must match y_values size ({len(self.y_values)}).",
                code="QST-VAL-701",
            )


@dataclass(frozen=True)
class ScatterSeries:
    """Immutable dataset model representing a scatter plot series."""

    label: str
    x_values: tuple[float, ...]
    y_values: tuple[float, ...]

    def __post_init__(self) -> None:
        """Validate alignment of coordinates."""
        from qst.exceptions.validation import ValidationError

        if len(self.x_values) != len(self.y_values):
            raise ValidationError(
                f"ScatterSeries x_values size ({len(self.x_values)}) must match y_values size ({len(self.y_values)}).",
                code="QST-VAL-701",
            )


@dataclass(frozen=True)
class HistogramSeries:
    """Immutable dataset model representing histogram bin distributions."""

    label: str
    values: tuple[float, ...]
    bin_edges: tuple[float, ...]
    bin_counts: tuple[int, ...]

    def __post_init__(self) -> None:
        """Validate histogram bins alignment."""
        from qst.exceptions.validation import ValidationError

        if len(self.bin_edges) != len(self.bin_counts) + 1:
            raise ValidationError(
                f"HistogramSeries bin_edges size ({len(self.bin_edges)}) must equal bin_counts size ({len(self.bin_counts)}) + 1.",
                code="QST-VAL-702",
            )


@dataclass(frozen=True)
class HeatmapMatrix:
    """Immutable dataset model representing a two-dimensional heatmap matrix."""

    label: str
    x_labels: tuple[str, ...]
    y_labels: tuple[str, ...]
    matrix: tuple[tuple[float, ...], ...]

    def __post_init__(self) -> None:
        """Validate matrix axes mapping dimensions."""
        from qst.exceptions.validation import ValidationError

        if len(self.matrix) != len(self.y_labels):
            raise ValidationError(
                f"HeatmapMatrix rows ({len(self.matrix)}) must match y_labels ({len(self.y_labels)}).",
                code="QST-VAL-703",
            )
        for idx, row in enumerate(self.matrix):
            if len(row) != len(self.x_labels):
                raise ValidationError(
                    f"HeatmapMatrix row {idx} size ({len(row)}) must match x_labels ({len(self.x_labels)}).",
                    code="QST-VAL-704",
                )
