"""End-to-End Pipeline test.

References:
    Docs/00_PROJECT_CONSTITUTION.md
    Docs/14_TESTING_STRATEGY.md
"""

import os
import json
import pytest
from qst.models.config import SimulationConfig, ProtocolType
from qst.orchestration.orchestrator import SimulationOrchestrator
from qst.orchestration.sweep_generator import ParameterSweepGenerator
from qst.models.results import SweepDimensions
from qst.analysis.trends.trends import TrendAnalysisService
from qst.reporting.serializers.serializers import ParameterSweepSerializer
from qst.reporting.exporters.json_exporter import JSONExporter
from qst.visualization.matplotlib_backend import MatplotlibBackend
from qst.visualization.styles import LightTheme
from qst.visualization.visualizer import Visualizer


@pytest.mark.e2e
def test_full_pipeline_e2e(tmp_path) -> None:
    """Verify end-to-end execution flow of QST pipeline from simulation to plotting."""
    # 1. Run simulation sweep
    qubit_counts = [10, 20]
    probabilities = [0.0, 0.5]
    seeds = [42]
    repetitions = 2

    configs = ParameterSweepGenerator.generate_configs(
        qubit_counts=qubit_counts,
        interception_probabilities=probabilities,
        seeds=seeds,
        repetitions=repetitions,
    )
    sweep_dims = SweepDimensions(
        qubit_counts=tuple(qubit_counts),
        interception_probabilities=tuple(probabilities),
        seeds=tuple(seeds),
    )

    orchestrator = SimulationOrchestrator()
    sweep_res = orchestrator.run_parameter_sweep(configs, sweep_dims)

    # 2. Assert statistics
    assert sweep_res.total_experiments == 4
    assert sweep_res.experiments[0].secure_runs == 2  # No interception
    exp_interception = sweep_res.experiments[1]
    assert exp_interception.secure_runs + exp_interception.warning_runs + exp_interception.compromised_runs == 2

    # 3. Analyze trends
    trend_service = TrendAnalysisService()
    line_series = trend_service.analyze_qber_vs_interception(sweep_res)

    assert line_series.label == "QBER vs Interception Probability"
    assert line_series.x_values == (0.0, 0.5)
    # Average QBER under 0 interception must be 0
    assert line_series.y_values[0] == 0.0
    # Average QBER under 0.5 interception must be positive
    assert line_series.y_values[1] > 0.0

    # 4. Serialize and Export
    serialized = ParameterSweepSerializer().serialize(sweep_res)
    json_path = os.path.join(tmp_path, "sweep_result.json")
    JSONExporter(overwrite_protection=False).export(
        filepath=json_path,
        data=serialized,
        metadata=serialized.get("metadata", {}),
    )

    assert os.path.exists(json_path)

    # 5. Visualize and render figure
    backend = MatplotlibBackend(overwrite_protection=False)
    theme = LightTheme()
    visualizer = Visualizer(backend, theme)

    plot_path = os.path.join(tmp_path, "qber_vs_interception.png")
    vis_res = visualizer.line_chart(line_series, plot_path)

    assert os.path.exists(plot_path)
    assert os.path.getsize(plot_path) > 0
    assert vis_res.format == "PNG"
