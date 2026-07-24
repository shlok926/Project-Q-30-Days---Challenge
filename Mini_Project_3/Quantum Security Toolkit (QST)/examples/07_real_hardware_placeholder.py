"""Example 07: Real Hardware Integration Workflow (Placeholder / Future Roadmap).

================================================================================
META INFORMATION
================================================================================
Difficulty Level: Intermediate
Estimated Completion Time: 2 minutes
Concepts Demonstrated:
  - Intended workflow for execution on real quantum processors (QPUs)
  - IBM Quantum Runtime API design preview
  - Graceful import checks and package warning triggers
  - Roadmap status updates for Phase 12

================================================================================
REQUIREMENTS
================================================================================
  - Python 3.10+
  - Quantum Security Toolkit (QST) installed or in python path
  - (Optional Future) qiskit-ibm-runtime >= 0.20.0

================================================================================
COMMON TROUBLESHOOTING
================================================================================
  - IBM Quantum Service warning: This script runs in mock mode by default because real hardware support is targeted for Phase 12.
"""

import sys
from pathlib import Path

# Ensure the package is importable if running directly from the root
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from qst.models.config import SimulationConfig, ProtocolType
from qst.orchestration.orchestrator import SimulationOrchestrator


def main() -> None:
    """Demonstrates how to check for IBM Quantum Runtime support and targets real QPUs."""
    # Define outputs paths using pathlib
    base_dir = Path(__file__).resolve().parent
    logs_dir = base_dir / "outputs" / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)
    log_file = logs_dir / "07_real_hardware.log"

    print("--- Example 07: Real Hardware Integration Preview ---")
    print(f"Logging setup path: {log_file}\n")

    # 1. Gracefully check for Qiskit IBM Runtime library
    ibm_runtime_available = False
    try:
        # Intended future imports
        import qiskit_ibm_runtime
        from qiskit_ibm_runtime import QiskitRuntimeService, Estimator, Sampler

        ibm_runtime_available = True
    except ImportError:
        print("[Roadmap Preview Note]: 'qiskit-ibm-runtime' is not installed.")
        print(
            "Real hardware execution support via IBM Quantum Runtime will be fully enabled in Phase 12.\n"
        )

    # 2. Demonstrate future API execution design
    print("--- Design Pattern for QPU Execution ---")
    print(
        "To execute simulations on a physical quantum backend in the future, the flow will be:"
    )
    print("  1. Initialize configuration with target QPU provider.")
    print("  2. Load stored IBM Quantum API tokens.")
    print("  3. Pass QiskitRuntimeService instance to orchestrator.")
    print("  4. Monitor job status on real IBM Quantum queue.\n")

    print("Example API invocation structure (Phase 12):")
    api_demo = """
    # Inside Phase 12 codebase:
    # service = QiskitRuntimeService(channel="ibm_quantum", token="YOUR_IBM_TOKEN")
    # backend = service.least_busy(simulator=False, operational=True)
    # config = SimulationConfig(
    #     n_qubits=20,
    #     backend_service=service,
    #     backend_name=backend.name,
    #     protocol=ProtocolType.BB84
    # )
    # orchestrator = SimulationOrchestrator()
    # result = orchestrator.run_on_hardware(config)
    """
    print(api_demo)

    # Log execution status
    with open(log_file, "w", encoding="utf-8") as lf:
        lf.write(
            f"QST Example 07 QPU Roadmap Log\n"
            f"IBM Runtime Available: {ibm_runtime_available}\n"
            f"Scheduled Phase:        Phase 12\n"
        )

    print("Status logged successfully. Ready for future QPU integration!")


if __name__ == "__main__":
    main()

# ================================================================================
# EXPECTED OUTPUT (Mocked)
# ================================================================================
# --- Example 07: Real Hardware Integration Preview ---
# Logging setup path: .../examples/outputs/logs/07_real_hardware.log
#
# [Roadmap Preview Note]: 'qiskit-ibm-runtime' is not installed.
# Real hardware execution support via IBM Quantum Runtime will be fully enabled in Phase 12.
#
# --- Design Pattern for QPU Execution ---
# ...
