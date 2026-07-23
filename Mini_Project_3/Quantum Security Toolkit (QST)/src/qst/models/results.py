"""Simulation result model and batch result domain definitions.

References:
    Docs/10_API_SPECIFICATION.md §5
    Docs/EXPORT_SPEC.md §1, §2
    Docs/QBER_SPEC.md §6
"""

from dataclasses import dataclass, field
from typing import Any, Optional

from qst.exceptions.validation import ValidationError
from qst.models.metadata import SimulationMetadata


@dataclass(frozen=True)
class SimulationResult:
    """The canonical output payload representing a single key-exchange simulation.

    Attributes:
        qber: Estimated Quantum Bit Error Rate, or None if no bits sifted.
        final_key_length: Size of final sifted and checked key.
        key_rate: Ratio of final key length to total raw qubits simulated.
        sifted_key: List of resulting shared secret key bits.
        n_qubits: Total qubits processed.
        seed: Random seed used in the run.
        eve_intercept_probability: Configured probability of interception.
        warnings: List of warnings raised during execution.
        metadata: Serialization-ready diagnostic metadata.
    """

    qber: Optional[float]
    final_key_length: int
    key_rate: float
    sifted_key: list[int]
    n_qubits: int
    seed: Optional[int]
    eve_intercept_probability: float
    warnings: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        """Validate output properties post initialization."""
        if self.qber is not None and not (0.0 <= self.qber <= 1.0):
            raise ValidationError(
                f"QBER must be between 0.0 and 1.0, got {self.qber}",
                code="QST-VAL-501",
            )
        if not (0.0 <= self.key_rate <= 1.0):
            raise ValidationError(
                f"Key rate must be between 0.0 and 1.0, got {self.key_rate}",
                code="QST-VAL-502",
            )
        if self.final_key_length < 0:
            raise ValidationError(
                f"Final key length must be non-negative, got {self.final_key_length}",
                code="QST-VAL-503",
            )


@dataclass(frozen=True)
class BatchResult:
    """Aggregated output containing multiple simulation run outcomes.

    Attributes:
        run_count: Total sweep run trials executed.
        results: Collection of individual SimulationResult objects.
    """

    run_count: int
    results: list[SimulationResult]

    def __post_init__(self) -> None:
        """Verify run count matches internal collection size."""
        if self.run_count != len(self.results):
            raise ValidationError(
                f"Run count ({self.run_count}) does not match results size ({len(self.results)})",
                code="QST-VAL-504",
            )


@dataclass(frozen=True)
class ExportMetadata:
    """Serialization formatting properties for exports.

    Attributes:
        format_type: Serialization codec identifier (e.g. 'json', 'csv').
        export_path: Output target file destination.
    """

    format_type: str
    export_path: str


@dataclass(frozen=True)
class ValidationResult:
    """Encapsulation representing validation check statuses.

    Attributes:
        is_valid: True if parameters successfully pass validators.
        error_message: Detailed message if parameters are invalid.
    """

    is_valid: bool
    error_message: Optional[str] = None
