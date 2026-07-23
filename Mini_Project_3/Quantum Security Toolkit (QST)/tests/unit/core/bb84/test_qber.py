"""Unit tests for the QBERService implementation.

References:
    Docs/QBER_SPEC.md §3, §4
    Docs/14_TESTING_STRATEGY.md §3
"""

import pytest

from qst.core.bb84.qber import QBERService
from qst.exceptions.validation import ValidationError
from qst.models.results import QBERResult


@pytest.mark.unit
def test_qber_perfect_transmission() -> None:
    """Verify QBER calculation for identical keys."""
    service = QBERService()
    alice = (1, 0, 1, 1, 0)
    bob = (1, 0, 1, 1, 0)

    res = service.calculate_qber(alice, bob)
    assert res.error_count == 0
    assert res.sifted_key_length == 5
    assert res.qber == 0.0
    assert "Warning" in res.confidence_notes  # short key warning < 10


@pytest.mark.unit
def test_qber_complete_mismatch() -> None:
    """Verify QBER calculation when all bits differ."""
    service = QBERService()
    alice = (1, 0, 1, 0)
    bob = (0, 1, 0, 1)

    res = service.calculate_qber(alice, bob)
    assert res.error_count == 4
    assert res.sifted_key_length == 4
    assert res.qber == 1.0


@pytest.mark.unit
def test_qber_intermediate() -> None:
    """Verify QBER calculation for normal partial errors."""
    service = QBERService()
    alice = (1, 0, 1, 1, 0, 0, 1, 1, 0, 0)
    bob = (1, 0, 1, 0, 0, 1, 1, 1, 0, 0)  # differences at index 3, 5

    res = service.calculate_qber(alice, bob)
    assert res.error_count == 2
    assert res.sifted_key_length == 10
    assert res.qber == 0.2
    assert "Normal" in res.confidence_notes  # key size >= 10


@pytest.mark.unit
def test_qber_empty_keys() -> None:
    """Verify empty keys return QBER=0.0 with confidence warnings."""
    service = QBERService()
    res = service.calculate_qber((), ())
    assert res.error_count == 0
    assert res.sifted_key_length == 0
    assert res.qber == 0.0
    assert "low" in res.confidence_notes


@pytest.mark.unit
def test_qber_validation_failures() -> None:
    """Verify that validator flags key mismatches or out of bound values."""
    service = QBERService()

    # Mismatched lengths
    with pytest.raises(ValidationError) as exc:
        service.calculate_qber((1, 0), (1,))
    assert "QST-VAL-805" in str(exc.value)

    # Invalid bits
    with pytest.raises(ValidationError) as exc:
        service.calculate_qber((1, 2), (1, 0))
    assert "QST-VAL-601" in str(exc.value)


@pytest.mark.unit
def test_qber_result_validation() -> None:
    """Verify QBERResult invariants and field bounds checks."""
    # Negative error count
    with pytest.raises(ValidationError) as exc:
        QBERResult(error_count=-1, sifted_key_length=5, qber=0.0, confidence_notes="")
    assert "QST-VAL-515" in str(exc.value)

    # Negative key length
    with pytest.raises(ValidationError) as exc:
        QBERResult(error_count=1, sifted_key_length=-1, qber=0.2, confidence_notes="")
    assert "QST-VAL-503" in str(exc.value)

    # QBER out of bounds
    with pytest.raises(ValidationError) as exc:
        QBERResult(error_count=1, sifted_key_length=5, qber=1.5, confidence_notes="")
    assert "QST-VAL-501" in str(exc.value)
