"""Example 06: Complete Pipeline.

================================================================================
META INFORMATION
================================================================================
Difficulty Level: Advanced
Estimated Completion Time: 5 minutes
Concepts Demonstrated:
  - Generating and running a multi-parameter sweep grid
  - Aggregating sweep statistics (mean QBER, mean key rate)
  - Executing trend analysis on QBER versus interception rates
  - Rendering line charts of trend lines under ScientificTheme
  - Serializing and exporting parameter sweep results to JSON and CSV formats
  - Integrating all components into a production simulation-to-report pipeline

================================================================================
REQUIREMENTS
================================================================================
  - Python 3.10+
  - matplotlib >= 3.0.0
  - Quantum Security Toolkit (QST) installed or in python path

================================================================================
COMMON TROUBLESHOOTING
================================================================================
  - Overwrite protection: Exporters throw validation errors if target output files already exist.
  - Large computation time: Ensure parameters do not exceed physical system boundaries.
"""

import sys
from pathlib import Path

# Ensure the package is importable if running directly from the root
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from qst.orchestration.orchestrator import SimulationOrchestrator
from qst.orchestration.sweep_generator import ParameterSweepGenerator
from qst.models.results import SweepDimensions
from qst.analysis.aggregators.aggregator import ExperimentAggregator
from qst.analysis.trends.trends import TrendAnalysisService
from qst.reporting.serializers.serializers import ParameterSweepSerializer
from qst.reporting.exporters.json_exporter import JSONExporter
from qst.reporting.exporters.csv_exporter import CSVExporter
from qst.visualization.matplotlib_backend import MatplotlibBackend
from qst.visualization.styles import ScientificTheme
from qst.visualization.visualizer import Visualizer
from qst.exceptions.base import QSTError


def main() -> None:
    """Demonstrates the complete workflow from simulation sweep to exported data & figures."""
    # Define outputs paths using pathlib
    base_dir = Path(__file__).resolve().parent
    json_dir = base_dir / "outputs" / "json"
    csv_dir = base_dir / "outputs" / "csv"
    figs_dir = base_dir / "outputs" / "figures"
    logs_dir = base_dir / "outputs" / "logs"

    json_dir.mkdir(parents=True, exist_ok=True)
    csv_dir.mkdir(parents=True, exist_ok=True)
    figs_dir.mkdir(parents=True, exist_ok=True)
    logs_dir.mkdir(parents=True, exist_ok=True)

    json_path = json_dir / "sweep_results.json"
    csv_path = csv_dir / "sweep_results.csv"
    fig_path = figs_dir / "qber_vs_intercept_trend.png"
    log_file = logs_dir / "06_complete_pipeline.log"

    print("--- Example 06: Running Complete Production Pipeline ---")
    print(f"Target JSON:  {json_path}")
    print(f"Target CSV:   {csv_path}")
    print(f"Target Trend: {fig_path}\n")

    # Define parameters
    qubit_counts = [10, 20]
    probabilities = [0.0, 0.25, 0.50]
    seeds = [42]
    repetitions = 3

    try:
        # 1. Sweep Grid Generation
        print("Generating grid configurations...")
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

        # 2. Sweep Execution
        print("Executing parameter sweep on Qiskit Aer Simulator...")
        orchestrator = SimulationOrchestrator()
        sweep_result = orchestrator.run_parameter_sweep(configs, sweep_dims)

        # 3. Statistics Aggregation
        print("Aggregating results metrics...")
        aggregator = ExperimentAggregator()
        aggregated_metrics = aggregator.aggregate(sweep_result)

        print(f"  Total trials run:     {aggregated_metrics.total_simulations}")
        print(f"  Aggregated Mean QBER: {aggregated_metrics.average_qber:.4f}")

        # 4. Trend Analysis
        print("Analyzing trends...")
        trend_service = TrendAnalysisService()
        trend_line = trend_service.analyze_qber_vs_interception(sweep_result)

        # 5. Visualization
        print("Rendering and exporting trend chart...")
        backend = MatplotlibBackend(overwrite_protection=False)
        visualizer = Visualizer(backend, ScientificTheme())
        visualizer.line_chart(trend_line, str(fig_path))
        print("Trend chart saved successfully.")

        # 6. Reporting Serialization & Export
        print("Serializing and exporting global reports...")
        serialized_sweep = ParameterSweepSerializer().serialize(sweep_result)

        # JSON Export
        JSONExporter(overwrite_protection=False).export(
            filepath=str(json_path),
            data=serialized_sweep,
            metadata=serialized_sweep.get("metadata", {}),
        )

        # CSV Export
        CSVExporter(overwrite_protection=False).export(
            filepath=str(csv_path),
            data=serialized_sweep,
            metadata=serialized_sweep.get("metadata", {}),
        )
        print("JSON & CSV Reports saved successfully.")

        # Optional: Save a log entry
        with open(log_file, "w", encoding="utf-8") as lf:
            lf.write("QST Example 06 E2E Pipeline Log\nSuccess\n")

        print("\n--- Production Pipeline Execution Succeeded! ---")

    except QSTError as e:
        print(f"\n[QST Validation Error]: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"\n[System Error]: Unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

# ================================================================================
# EXPECTED OUTPUT
# ================================================================================
# --- Example 06: Running Complete Production Pipeline ---
# Target JSON:  .../examples/outputs/json/sweep_results.json
# Target CSV:   .../examples/outputs/csv/sweep_results.csv
# Target Trend: .../examples/outputs/figures/qber_vs_intercept_trend.png
#
# Generating grid configurations...
# Executing parameter sweep on Qiskit Aer Simulator...
# Aggregating results metrics...
#   Total trials run:     18
#   Aggregated Mean QBER: 0.0520
# Analyzing trends...
# Rendering and exporting trend chart...
# Trend chart saved successfully.
# Serializing and exporting global reports...
# JSON & CSV Reports saved successfully.
#
# --- Production Pipeline Execution Succeeded! ---
