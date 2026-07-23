"""SimulationConfig domain model for QST.

References:
    Docs/10_API_SPECIFICATION.md §3
    Docs/05_PRODUCT_REQUIREMENTS.md §1
"""

from dataclasses import dataclass
from typing import Optional

from qst.utils.validation import (
    validate_probability,
    validate_qubit_count,
    validate_seed,
)


@dataclass(frozen=True)
class SimulationConfig:
    """Read-only parameter settings configuration for a single simulation run.

    Attributes:
        n_qubits: Number of qubits to simulate.
        seed: Random seed for reproducibility.
        eve_intercept_probability: Probability of eavesdropper interception.
    """

    n_qubits: int
    seed: Optional[int] = None
    eve_intercept_probability: float = 0.0

    def __post_init__(self) -> None:
        """Perform validation on configured parameters after initialization."""
        validate_qubit_count(self.n_qubits)
        validate_seed(self.seed)
        validate_probability(
            self.eve_intercept_probability, name="eve_intercept_probability"
        )
