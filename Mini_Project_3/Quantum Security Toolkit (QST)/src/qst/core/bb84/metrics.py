"""Security Metrics Service implementation.

References:
    Docs/QBER_SPEC.md §4
    Docs/11_SECURITY_ARCHITECTURE.md §4
"""

from typing import Optional

from qst.models.config import SecurityThresholds
from qst.models.results import (
    QBERResult,
    ReconciliationResult,
    SecurityMetrics,
    SecurityStatus,
)


class SecurityMetricsService:
    """Computes channel transmission rates and evaluates status classifications."""

    def __init__(self, thresholds: Optional[SecurityThresholds] = None) -> None:
        """Initialize the SecurityMetricsService.

        Args:
            thresholds: Threshold settings for security status checks.
        """
        self._thresholds = thresholds or SecurityThresholds()

    def compute_metrics(
        self,
        n_qubits: int,
        reconciliation_result: ReconciliationResult,
        qber_result: QBERResult,
    ) -> SecurityMetrics:
        """Evaluate key rate, discard rate, error rate, and overall security status.

        Args:
            n_qubits: Total number of simulated raw qubits.
            reconciliation_result: Calculated reconciliation details.
            qber_result: Computed QBER metrics.

        Returns:
            A SecurityMetrics domain object containing security classifications.
        """
        if n_qubits <= 0:
            return SecurityMetrics(
                key_rate=0.0,
                discard_rate=0.0,
                error_rate=0.0,
                status=SecurityStatus.SECURE,
            )

        sifted_len = qber_result.sifted_key_length
        key_rate = float(sifted_len / n_qubits)

        # Discard rate is the ratio of discarded bits during reconciliation to total bits
        discard_count = len(reconciliation_result.discarded_indices)
        discard_rate = float(discard_count / n_qubits)

        error_rate = qber_result.qber

        # Classification decision logic based on QBER vs thresholds
        if error_rate <= self._thresholds.secure_qber:
            status = SecurityStatus.SECURE
        elif error_rate <= self._thresholds.warning_qber:
            status = SecurityStatus.WARNING
        else:
            status = SecurityStatus.COMPROMISED

        return SecurityMetrics(
            key_rate=key_rate,
            discard_rate=discard_rate,
            error_rate=error_rate,
            status=status,
        )
