"""Example 02: Eavesdropper Demonstration.

================================================================================
META INFORMATION
================================================================================
Difficulty Level: Intermediate
Estimated Completion Time: 3 minutes
Concepts Demonstrated:
  - Eve intercept-resend attack simulation
  - Measuring Quantum Bit Error Rate (QBER) shift across interception rates
  - Observing status transitions (SECURE -> WARNING -> COMPROMISED)
  - Understanding quantum measurement collapse theory

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
  - Interception Probabilities out of range: Ensure values are between 0.0 and 1.0.
  - Large execution delays: Higher repetitions increase simulator computation time.
"""

import sys
from pathlib import Path

# Ensure the package is importable if running directly from the root
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from qst.models.config import SimulationConfig, ProtocolType
from qst.orchestration.orchestrator import SimulationOrchestrator
from qst.exceptions.base import QSTError


def main() -> None:
    """Runs BB84 simulations with varying interception probabilities and prints metrics."""
    # Define outputs and log directories
    base_dir = Path(__file__).resolve().parent
    logs_dir = base_dir / "outputs" / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)
    log_file = logs_dir / "02_eavesdropper_demo.log"

    print("--- Example 02: Eavesdropper Demonstration ---")
    print(f"Logging setup path: {log_file}\n")

    # Define test parameters
    probabilities = [0.0, 0.25, 0.50, 0.75, 1.0]
    n_qubits = 20
    seed = 8888
    repetitions = 5

    orchestrator = SimulationOrchestrator()

    header = f"{'Intercept Prob':<16} | {'Avg QBER':<10} | {'Status':<12} | {'Key Length (Avg)':<16}"
    print(header)
    print("-" * len(header))

    try:
        log_entries = []
        for p in probabilities:
            # 1. Initialize configuration for this interception rate
            config = SimulationConfig(
                n_qubits=n_qubits,
                seed=seed,
                interception_probability=p,
                repetitions=repetitions,
                protocol=ProtocolType.BB84,
            )

            # 2. Run simulation batch
            res = orchestrator.run_many(config)

            # Compute average key length for this batch
            avg_key_len = sum(sim.final_key_length for sim in res.simulations) / len(
                res.simulations
            )

            # Print trial results
            status_str = res.simulations[0].security_metrics.status.value
            row = f"{p:<16.2f} | {res.average_qber:<10.4f} | {status_str:<12} | {avg_key_len:<16.2f}"
            print(row)
            log_entries.append(row)

        # Write log summaries
        with open(log_file, "w", encoding="utf-8") as lf:
            lf.write("QST Example 02 Run Log\n")
            lf.write(header + "\n")
            lf.write("\n".join(log_entries) + "\n")

        # 3. Print scientific discussion
        print("\n--- Physical Discussion: Quantum State Collapse ---")
        print(
            "In quantum mechanics, measuring a state collapses it onto one of the basis eigenstates."
        )
        print("When Eve intercepts a qubit:")
        print(
            "  1. If she guesses Alice's basis correctly, she obtains the bit without introducing errors."
        )
        print(
            "  2. If she guesses incorrectly, she projects the qubit onto a mismatched basis."
        )
        print(
            "When Bob subsequently measures the qubit, he will get a random outcome, introducing a 50% error probability."
        )
        print(
            "Since Eve guesses correctly with 50% probability, the theoretical error rate is 25% under a full attack."
        )
        print(
            "QST detects this QBER increase and automatically flags the channel as 'COMPROMISED'."
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
# --- Example 02: Eavesdropper Demonstration ---
# Logging setup path: .../examples/outputs/logs/02_eavesdropper_demo.log
#
# Intercept Prob    | Avg QBER   | Status       | Key Length (Avg)
# ------------------------------------------------------------------
# 0.00             | 0.0000     | SECURE       | 9.40
# 0.25             | 0.0719     | SECURE       | 9.80
# 0.50             | 0.1246     | WARNING      | 10.20
# 0.75             | 0.1788     | COMPROMISED  | 9.20
# 1.00             | 0.2559     | COMPROMISED  | 9.80
#
# --- Physical Discussion: Quantum State Collapse ---
# ...
