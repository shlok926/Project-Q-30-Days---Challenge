"""SimulationConfig domain model for QST.

References:
    Docs/10_API_SPECIFICATION.md §3
    Docs/05_PRODUCT_REQUIREMENTS.md §1
"""

from dataclasses import dataclass
from typing import Optional

from qst.exceptions.validation import ValidationError
from qst.utils.validation import (
    validate_probability,
    validate_qubit_count,
    validate_seed,
)


@dataclass(frozen=True)
class SecurityThresholds:
    """Configurable security threshold limits for QKD runs.

    Attributes:
        secure_qber: Maximum QBER limit to classify channel as secure.
        warning_qber: QBER limit above which the channel is compromised.
    """

    secure_qber: float = 0.0
    warning_qber: float = 0.11

    def __post_init__(self) -> None:
        """Validate thresholds ranges."""
        validate_probability(self.secure_qber, name="secure_qber")
        validate_probability(self.warning_qber, name="warning_qber")
        if self.secure_qber > self.warning_qber:
            raise ValidationError(
                f"secure_qber ({self.secure_qber}) cannot be greater than warning_qber ({self.warning_qber}).",
                code="QST-VAL-302",
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
