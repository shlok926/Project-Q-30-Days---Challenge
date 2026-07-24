"""Example 03: Parameter Sweep.

================================================================================
META INFORMATION
================================================================================
Difficulty Level: Intermediate
Estimated Completion Time: 4 minutes
Concepts Demonstrated:
  - Generating grid configs via ParameterSweepGenerator
  - Executing parameter sweeps via SimulationOrchestrator
  - Processing and aggregating sweep metrics using ExperimentAggregator
  - Reviewing statistical metrics (mean QBER, mean key rate, throughput)

================================================================================
REQUIREMENTS
================================================================================
  - Python 3.10+
  - qiskit >= 1.0.0
  - qiskit-aer >= 0.14.0
  - Quantum Security Toolkit (QST) installed or in python path

================================================================================
COMMON TROUBLESHOOTING
================================================================================
  - Config Grid Too Large: Restrict parameter ranges to avoid long wait times.
  - Non-deterministic outcomes: Pass a list containing a fixed seed (e.g. `[42]`).
"""

import sys
from pathlib import Path

# Ensure the package is importable if running directly from the root
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from qst.orchestration.orchestrator import SimulationOrchestrator
from qst.orchestration.sweep_generator import ParameterSweepGenerator
from qst.models.results import SweepDimensions
from qst.analysis.aggregators.aggregator import ExperimentAggregator
from qst.exceptions.base import QSTError


def main() -> None:
    """Executes a parameter sweep over qubit counts and interception probabilities."""
    # Define outputs and log directories
    base_dir = Path(__file__).resolve().parent
    logs_dir = base_dir / "outputs" / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)
    log_file = logs_dir / "03_parameter_sweep.log"

    print("--- Example 03: Running Parameter Sweeps and Aggregations ---")
    print(f"Logging setup path: {log_file}\n")

    # 1. Define sweep parameter values
    qubit_counts = [10, 20]
    probabilities = [0.0, 0.4]
    seeds = [42]
    repetitions = 3

    print(f"Parameter grid details:")
    print(f"  Qubit Counts:               {qubit_counts}")
    print(f"  Interception Probabilities: {probabilities}")
    print(f"  Repetitions per config:     {repetitions}")

    try:
        # 2. Generate configuration lists
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

        # 3. Run parameter sweep using Orchestrator
        orchestrator = SimulationOrchestrator()
        sweep_result = orchestrator.run_parameter_sweep(configs, sweep_dims)

        # 4. Compile statistics via Aggregator
        aggregator = ExperimentAggregator()
        aggregated = aggregator.aggregate(sweep_result)

        # 5. Display key telemetry
        print("\n--- Sweep Execution Telemetry: ---")
        print(f"Total Configurations Run: {sweep_result.total_experiments}")
        print(f"Total Simulation Trials:  {aggregated.total_simulations}")
        print(f"Mean QBER (Error Rate):   {aggregated.average_qber:.4f}")
        print(f"Mean Key Rate:            {aggregated.average_key_rate:.4f}")
        print(
            f"Aggregated Throughput:    {aggregated.average_throughput:.2f} qubits/sec"
        )
        print(f"Success Ratio (Secure):   {aggregated.success_ratio:.2f}")

        # Optional: Save a log entry
        with open(log_file, "w", encoding="utf-8") as lf:
            lf.write(
                f"QST Example 03 Sweep Log\n"
                f"Total Experiments: {sweep_result.total_experiments}\n"
                f"Mean QBER:         {aggregated.average_qber}\n"
                f"Throughput:        {aggregated.average_throughput}\n"
            )

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
# --- Example 03: Running Parameter Sweeps and Aggregations ---
# Logging setup path: .../examples/outputs/logs/03_parameter_sweep.log
#
# Parameter grid details:
#   Qubit Counts:               [10, 20]
#   Interception Probabilities: [0.0, 0.4]
#   Repetitions per config:     3
#
# --- Sweep Execution Telemetry: ---
# Total Configurations Run: 4
# Total Simulation Trials:  12
# Mean QBER (Error Rate):   0.0526  (Will vary slightly depending on random outcomes)
# Mean Key Rate:            0.4306
# Aggregated Throughput:    ... qubits/sec
# Success Ratio (Secure):   0.50
