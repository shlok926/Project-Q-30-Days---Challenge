"""Visualization package initialization exposing backends, registry, themes, and datasets.

References:
    Docs/07_SYSTEM_ARCHITECTURE.md §5, §11
"""

from qst.visualization.visualizer import Visualizer
from qst.visualization.backend import (
    VisualizationBackend,
    VisualizationResult,
    ChartType,
)
from qst.visualization.matplotlib_backend import MatplotlibBackend
from qst.visualization.registry import VisualizationBackendRegistry
from qst.visualization.styles import (
    Theme,
    LightTheme,
    DarkTheme,
    ScientificTheme,
    Typography,
    Colors,
    GridStyle,
    FigureStyle,
)
from qst.visualization.datasets import (
    ImageFormat,
    LineSeries,
    ScatterSeries,
    HistogramSeries,
    HeatmapMatrix,
)

__all__ = [
    "Visualizer",
    "VisualizationBackend",
    "VisualizationResult",
    "ChartType",
    "MatplotlibBackend",
    "VisualizationBackendRegistry",
    "Theme",
    "LightTheme",
    "DarkTheme",
    "ScientificTheme",
    "Typography",
    "Colors",
    "GridStyle",
    "FigureStyle",
    "ImageFormat",
    "LineSeries",
    "ScatterSeries",
    "HistogramSeries",
    "HeatmapMatrix",
]
