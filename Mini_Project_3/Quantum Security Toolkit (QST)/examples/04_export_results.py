"""Example 04: Export Results.

================================================================================
META INFORMATION
================================================================================
Difficulty Level: Intermediate
Estimated Completion Time: 3 minutes
Concepts Demonstrated:
  - Running a QST simulation and serializing results using ExperimentSerializer
  - Exporting simulation results to JSON using JSONExporter
  - Exporting simulation results to CSV using CSVExporter
  - Loading exported files back and verifying metadata/schema integrity

================================================================================
REQUIREMENTS
================================================================================
  - Python 3.10+
  - Quantum Security Toolkit (QST) installed or in python path

================================================================================
COMMON TROUBLESHOOTING
================================================================================
  - Overwrite errors: `JSONExporter` and `CSVExporter` protect existing files. Pass `overwrite_protection=False` to force overwrite.
  - File Permissions: Ensure directories are writable.
"""

import sys
import json
import csv
from pathlib import Path

# Ensure the package is importable if running directly from the root
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from qst.models.config import SimulationConfig, ProtocolType
from qst.orchestration.orchestrator import SimulationOrchestrator
from qst.reporting.serializers.serializers import ExperimentSerializer
from qst.reporting.exporters.json_exporter import JSONExporter
from qst.reporting.exporters.csv_exporter import CSVExporter
from qst.exceptions.base import QSTError


def main() -> None:
    """Runs a simulation, serializes, exports to JSON/CSV, and re-loads them."""
    # Define outputs paths using pathlib
    base_dir = Path(__file__).resolve().parent
    json_dir = base_dir / "outputs" / "json"
    csv_dir = base_dir / "outputs" / "csv"
    logs_dir = base_dir / "outputs" / "logs"

    json_dir.mkdir(parents=True, exist_ok=True)
    csv_dir.mkdir(parents=True, exist_ok=True)
    logs_dir.mkdir(parents=True, exist_ok=True)

    json_path = json_dir / "simulation_run.json"
    csv_path = csv_dir / "simulation_run.csv"
    log_file = logs_dir / "04_export_results.log"

    print("--- Example 04: Exporting Simulation Results to JSON and CSV ---")
    print(f"Target JSON: {json_path}")
    print(f"Target CSV:  {csv_path}\n")

    try:
        # 1. Run simulation config
        config = SimulationConfig(
            n_qubits=15,
            seed=42,
            interception_probability=0.2,
            repetitions=1,
            protocol=ProtocolType.BB84,
        )
        orchestrator = SimulationOrchestrator()
        result = orchestrator.run_once(config)

        # 2. Serialize result using ExperimentSerializer
        serializer = ExperimentSerializer()
        serialized_data = serializer.serialize(result)

        # 3. Export to JSON (overwrites if it already exists)
        json_exporter = JSONExporter(overwrite_protection=False)
        json_exporter.export(
            filepath=str(json_path),
            data=serialized_data,
            metadata={"timestamp": "2026-07-24T17:15:00", "qiskit_version": "2.0.0"},
        )
        print("JSON Export completed successfully.")

        # 4. Export to CSV
        csv_exporter = CSVExporter(overwrite_protection=False)
        csv_exporter.export(
            filepath=str(csv_path),
            data=serialized_data,
            metadata={"timestamp": "2026-07-24T17:15:00", "qiskit_version": "2.0.0"},
        )
        print("CSV Export completed successfully.")

        # 5. Reload JSON and verify schema metadata
        print("\n--- Reloading JSON and Verifying Integrity ---")
        with open(json_path, "r", encoding="utf-8") as f:
            reloaded_json = json.load(f)

        print(f"Reloaded Schema Version: {reloaded_json.get('schema_version')}")
        print(f"Reloaded Metadata:       {reloaded_json.get('metadata')}")
        print(
            f"Average QBER in File:    {reloaded_json.get('data', {}).get('average_qber')}"
        )

        # 6. Reload CSV and verify columns
        print("\n--- Reloading CSV and Verifying Columns ---")
        with open(csv_path, "r", encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            print(f"CSV Total Rows:      {len(rows)}")
            print(f"CSV Column Headers:  {reader.fieldnames}")

        # Optional: Save a log entry
        with open(log_file, "w", encoding="utf-8") as lf:
            lf.write("QST Example 04 Export Log\nSuccess\n")

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
# --- Example 04: Exporting Simulation Results to JSON and CSV ---
# Target JSON: .../examples/outputs/json/simulation_run.json
# Target CSV:  .../examples/outputs/csv/simulation_run.csv
#
# JSON Export completed successfully.
# CSV Export completed successfully.
#
# --- Reloading JSON and Verifying Integrity ---
# Reloaded Schema Version: 1.0.0
# Reloaded Metadata:       {'timestamp': '2026-07-24T17:15:00', 'qiskit_version': '2.0.0'}
# Average QBER in File:    0.0
#
# --- Reloading CSV and Verifying Columns ---
# CSV Total Rows:      1
# CSV Column Headers:  ['timestamp', 'qiskit_version', 'experiment_average_qber', ...]
