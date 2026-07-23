"""Analysis package exposing aggregators, comparisons, and trends services.

References:
    Docs/10_API_SPECIFICATION.md §5
"""

from qst.analysis.aggregators.aggregator import (
    ExperimentAggregator,
    AggregationResult,
)
from qst.analysis.trends.trends import TrendAnalysisService
from qst.analysis.comparisons.comparison import (
    ComparisonService,
    ComparisonResult,
)

__all__ = [
    "ExperimentAggregator",
    "AggregationResult",
    "TrendAnalysisService",
    "ComparisonService",
    "ComparisonResult",
]
