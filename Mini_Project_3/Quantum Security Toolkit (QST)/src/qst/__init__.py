"""Quantum Security Toolkit (QST) package initialization.

References:
    Docs/00_PROJECT_CONSTITUTION.md
    Docs/07_SYSTEM_ARCHITECTURE.md
"""

from qst.config.settings import QST_VERSION
from qst.exceptions.base import QSTError
from qst.exceptions.validation import ValidationError
from qst.models.config import SimulationConfig, SecurityThresholds, ProtocolType
from qst.models.results import (
    SimulationResult,
    ExperimentMetadata,
    ExecutionMetrics,
    ExperimentResult,
    SweepDimensions,
    ParameterSweepResult,
    StatisticsResult,
)
from qst.orchestration.orchestrator import SimulationOrchestrator
from qst.orchestration.statistics import ExperimentStatisticsService
from qst.orchestration.sweep_generator import ParameterSweepGenerator
from qst.reporting.serializers.serializers import (
    ExportFormat,
    SimulationSerializer,
    ExperimentSerializer,
    ParameterSweepSerializer,
)
from qst.reporting.exporters.json_exporter import JSONExporter
from qst.reporting.exporters.csv_exporter import CSVExporter
from qst.analysis.aggregators.aggregator import (
    ExperimentAggregator,
    AggregationResult,
)
from qst.analysis.trends.trends import TrendAnalysisService
from qst.analysis.comparisons.comparison import (
    ComparisonService,
    ComparisonResult,
)
from qst.visualization.datasets import (
    LineSeries,
    ScatterSeries,
    HistogramSeries,
    HeatmapMatrix,
)
from qst.visualization.backend import VisualizationBackend, VisualizationResult
from qst.visualization.matplotlib_backend import MatplotlibBackend
from qst.visualization.registry import VisualizationBackendRegistry
from qst.visualization.styles import Theme, LightTheme, DarkTheme, ScientificTheme

__version__ = QST_VERSION

__all__ = [
    "SimulationOrchestrator",
    "SimulationResult",
    "QSTError",
    "ValidationError",
    "SimulationConfig",
    "SecurityThresholds",
    "ProtocolType",
    "ExperimentMetadata",
    "ExecutionMetrics",
    "ExperimentResult",
    "SweepDimensions",
    "ParameterSweepResult",
    "StatisticsResult",
    "ExperimentStatisticsService",
    "ParameterSweepGenerator",
    "ExportFormat",
    "SimulationSerializer",
    "ExperimentSerializer",
    "ParameterSweepSerializer",
    "JSONExporter",
    "CSVExporter",
    "ExperimentAggregator",
    "AggregationResult",
    "TrendAnalysisService",
    "ComparisonService",
    "ComparisonResult",
    "LineSeries",
    "ScatterSeries",
    "HistogramSeries",
    "HeatmapMatrix",
    "VisualizationBackend",
    "VisualizationResult",
    "MatplotlibBackend",
    "VisualizationBackendRegistry",
    "Theme",
    "LightTheme",
    "DarkTheme",
    "ScientificTheme",
]
