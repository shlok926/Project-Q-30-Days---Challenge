"""Example 01: Basic BB84 Simulation.

================================================================================
META INFORMATION
================================================================================
Difficulty Level: Beginner
Estimated Completion Time: 2 minutes
Concepts Demonstrated:
  - Creating a SimulationConfig
  - Running a single-trial BB84 quantum simulation
  - Reading SimulationResult metrics (key rate, discard rate, QBER, security status)
  - Handling execution logging and outputs path integration

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
  - QST-VAL-101 (Qubit count must be positive): Ensure `n_qubits` is > 0.
  - Aer Simulator Errors: Ensure qiskit-aer is installed correctly.
  - Separators / Paths: Use `pathlib` for file routing to prevent crash.
"""

import sys
from pathlib import Path

# Ensure the package is importable if running directly from the root
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from qst.models.config import SimulationConfig, ProtocolType
from qst.orchestration.orchestrator import SimulationOrchestrator
from qst.exceptions.base import QSTError


def main() -> None:
    """Executes a simple single BB84 simulation trial with fixed seed."""
    # Define outputs and log directories
    base_dir = Path(__file__).resolve().parent
    logs_dir = base_dir / "outputs" / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)
    log_file = logs_dir / "01_basic_bb84.log"

    print("--- Example 01: Running Single BB84 Quantum Simulation ---")
    print(f"Logging setup path: {log_file}")

    try:
        # 1. Initialize configuration with deterministic seed
        config = SimulationConfig(
            n_qubits=15,
            seed=42,
            interception_probability=0.0,  # No eavesdropping for this baseline run
            repetitions=1,
            protocol=ProtocolType.BB84,
        )

        print(f"Configured qubits: {config.n_qubits}")
        print(f"Interception probability: {config.interception_probability}")
        print(f"Deterministic seed: {config.seed}")

        # 2. Run simulation via Orchestrator
        orchestrator = SimulationOrchestrator()
        experiment_result = orchestrator.run_once(config)

        # 3. Read trial results from the experiment
        trial_result = experiment_result.simulations[0]

        # 4. Print metrics to console
        print("\n--- Simulation Complete. Metrics: ---")
        print(f"Sifted Key Length: {trial_result.final_key_length} bits")
        print(
            f"Key Rate:          {trial_result.key_rate:.4f} (sifted key / total qubits)"
        )
        print(
            f"Discard Rate:      {trial_result.security_metrics.discard_rate:.4f} (discarded / total qubits)"
        )
        print(f"QBER (Error Rate): {trial_result.qber:.4f}")
        print(f"Security Status:   {trial_result.security_metrics.status.value}")

        # Optional: Save a log entry
        with open(log_file, "w", encoding="utf-8") as lf:
            lf.write(
                f"QST Example 01 log\n"
                f"QBER: {trial_result.qber}\n"
                f"Key Rate: {trial_result.key_rate}\n"
                f"Status: {trial_result.security_metrics.status.value}\n"
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
# EXPECTED OUTPUT (Deterministic)
# ================================================================================
# --- Example 01: Running Single BB84 Quantum Simulation ---
# Logging setup path: .../examples/outputs/logs/01_basic_bb84.log
# Configured qubits: 15
# Interception probability: 0.0
# Deterministic seed: 42
#
# --- Simulation Complete. Metrics: ---
# Sifted Key Length: 7 bits
# Key Rate:          0.4667 (sifted key / total qubits)
# Discard Rate:      0.5333 (discarded / total qubits)
# QBER (Error Rate): 0.0000
# Security Status:   SECURE
