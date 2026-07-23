"""Unit tests for the SecurityMetricsService implementation.

References:
    Docs/QBER_SPEC.md §4
    Docs/11_SECURITY_ARCHITECTURE.md §4
    Docs/14_TESTING_STRATEGY.md §3
"""

import pytest

from qst.core.bb84.metrics import SecurityMetricsService
from qst.exceptions.validation import ValidationError
from qst.models.config import SecurityThresholds
from qst.models.results import (
    QBERResult,
    ReconciliationResult,
    SecurityMetrics,
    SecurityStatus,
)


@pytest.mark.unit
def test_security_metrics_transitions() -> None:
    """Verify classification transitions (Secure -> Warning -> Compromised) at 0.0 and 0.11."""
    # Use default thresholds: secure_qber = 0.0, warning_qber = 0.11
    service = SecurityMetricsService()

    recon = ReconciliationResult(
        matching_indices=(0, 1, 2, 3),
        discarded_indices=(4, 5),
        matching_bases=("Z", "Z", "X", "X"),
        total_bits=6,
        matching_count=4,
        match_rate=4 / 6,
    )

    # 1. SECURE classification (QBER = 0.0)
    qber_secure = QBERResult(
        error_count=0, sifted_key_length=4, qber=0.0, confidence_notes=""
    )
    metrics_sec = service.compute_metrics(6, recon, qber_secure)
    assert metrics_sec.status == SecurityStatus.SECURE
    assert metrics_sec.key_rate == 4 / 6
    assert metrics_sec.discard_rate == 2 / 6
    assert metrics_sec.error_rate == 0.0

    # 2. WARNING classification (QBER = 0.10)
    qber_warning = QBERResult(
        error_count=1, sifted_key_length=10, qber=0.10, confidence_notes=""
    )
    metrics_warn = service.compute_metrics(10, recon, qber_warning)
    assert metrics_warn.status == SecurityStatus.WARNING

    # 3. COMPROMISED classification (QBER = 0.12)
    qber_compromised = QBERResult(
        error_count=3, sifted_key_length=25, qber=0.12, confidence_notes=""
    )
    metrics_comp = service.compute_metrics(25, recon, qber_compromised)
    assert metrics_comp.status == SecurityStatus.COMPROMISED


@pytest.mark.unit
def test_security_metrics_custom_thresholds() -> None:
    """Verify custom SecurityThresholds alter classification decision boundaries."""
    # Secure limit is 0.02, Warning limit is 0.08
    thresh = SecurityThresholds(secure_qber=0.02, warning_qber=0.08)
    service = SecurityMetricsService(thresh)

    recon = ReconciliationResult(
        matching_indices=(0,),
        discarded_indices=(),
        matching_bases=("Z",),
        total_bits=1,
        matching_count=1,
        match_rate=1.0,
    )

    # QBER is 0.01 <= 0.02 (SECURE)
    qber_sec = QBERResult(
        error_count=1, sifted_key_length=100, qber=0.01, confidence_notes=""
    )
    metrics_sec = service.compute_metrics(100, recon, qber_sec)
    assert metrics_sec.status == SecurityStatus.SECURE

    # QBER is 0.05 (WARNING)
    qber_warn = QBERResult(
        error_count=5, sifted_key_length=100, qber=0.05, confidence_notes=""
    )
    metrics_warn = service.compute_metrics(100, recon, qber_warn)
    assert metrics_warn.status == SecurityStatus.WARNING

    # QBER is 0.09 (COMPROMISED)
    qber_comp = QBERResult(
        error_count=9, sifted_key_length=100, qber=0.09, confidence_notes=""
    )
    metrics_comp = service.compute_metrics(100, recon, qber_comp)
    assert metrics_comp.status == SecurityStatus.COMPROMISED


@pytest.mark.unit
def test_security_thresholds_validation() -> None:
    """Verify invalid threshold values trigger range and logic errors."""
    # Out of bounds probability
    with pytest.raises(ValidationError) as exc:
        SecurityThresholds(secure_qber=1.2, warning_qber=0.11)
    assert "QST-VAL-202" in str(exc.value)

    # secure_qber > warning_qber check
    with pytest.raises(ValidationError) as exc:
        SecurityThresholds(secure_qber=0.05, warning_qber=0.02)
    assert "QST-VAL-302" in str(exc.value)


@pytest.mark.unit
def test_security_metrics_zero_qubits() -> None:
    """Verify zero qubits handles empty transmission case gracefully."""
    service = SecurityMetricsService()
    recon = ReconciliationResult(
        matching_indices=(),
        discarded_indices=(),
        matching_bases=(),
        total_bits=0,
        matching_count=0,
        match_rate=0.0,
    )
    qber = QBERResult(error_count=0, sifted_key_length=0, qber=0.0, confidence_notes="")

    metrics = service.compute_metrics(0, recon, qber)
    assert metrics.key_rate == 0.0
    assert metrics.discard_rate == 0.0
    assert metrics.error_rate == 0.0
    assert metrics.status == SecurityStatus.SECURE


@pytest.mark.unit
def test_security_metrics_validation_ranges() -> None:
    """Verify SecurityMetrics dataclass checks metrics boundaries."""
    # Invalid Key Rate
    with pytest.raises(ValidationError) as exc:
        SecurityMetrics(
            key_rate=1.5,
            discard_rate=0.2,
            error_rate=0.01,
            status=SecurityStatus.SECURE,
        )
    assert "QST-VAL-502" in str(exc.value)

    # Invalid Discard Rate
    with pytest.raises(ValidationError) as exc:
        SecurityMetrics(
            key_rate=0.5,
            discard_rate=-0.1,
            error_rate=0.01,
            status=SecurityStatus.SECURE,
        )
    assert "QST-VAL-516" in str(exc.value)

    # Invalid Error Rate
    with pytest.raises(ValidationError) as exc:
        SecurityMetrics(
            key_rate=0.5,
            discard_rate=0.5,
            error_rate=1.05,
            status=SecurityStatus.SECURE,
        )
    assert "QST-VAL-517" in str(exc.value)
