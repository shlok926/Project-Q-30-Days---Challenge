"""SimulationMetadata model for QST.

References:
    Docs/10_API_SPECIFICATION.md §5
    Docs/EXPORT_SPEC.md §1
"""

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class SimulationMetadata:
    """Diagnostic and package execution metadata.

    Attributes:
        qst_version: Running version of the QST package.
        qiskit_version: Running version of the dependency Qiskit library.
        simulation_duration_seconds: Time taken to execute the simulation.
        extra: Additional flexible fields for diagnostic telemetry.
    """

    qst_version: str
    qiskit_version: str
    simulation_duration_seconds: float
    extra: dict[str, Any] = field(default_factory=dict)
