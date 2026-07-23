"""Unit tests for the QST BasisReconciliationService and ReconciliationStatistics.

References:
    Docs/BB84_SPEC.md §1 Step 7
    Docs/14_TESTING_STRATEGY.md §3
"""

import pytest

from qst.core.bb84.reconciliation import (
    BasisReconciliationService,
    ReconciliationStatistics,
)
from qst.exceptions.validation import ValidationError


@pytest.mark.unit
def test_reconciliation_statistics() -> None:
    """Verify statistics helper calculates correct counts and rates."""
    assert ReconciliationStatistics.match_rate(5, 10) == 0.5
    assert ReconciliationStatistics.match_rate(0, 0) == 0.0
    assert ReconciliationStatistics.discard_count(10, 3) == 7
    assert ReconciliationStatistics.discard_rate(7, 10) == 0.7
    assert ReconciliationStatistics.discard_rate(0, 0) == 0.0


@pytest.mark.unit
def test_reconcile_perfect_match() -> None:
    """Verify reconciliation when all bases match exactly."""
    service = BasisReconciliationService()
    alice = ("Z", "X", "Z", "X")
    bob = ("Z", "X", "Z", "X")

    res = service.reconcile(alice, bob)
    assert res.matching_indices == (0, 1, 2, 3)
    assert res.discarded_indices == ()
    assert res.matching_bases == ("Z", "X", "Z", "X")
    assert res.total_bits == 4
    assert res.matching_count == 4
    assert res.match_rate == 1.0


@pytest.mark.unit
def test_reconcile_no_match() -> None:
    """Verify reconciliation when no bases match."""
    service = BasisReconciliationService()
    alice = ("Z", "Z", "Z")
    bob = ("X", "X", "X")

    res = service.reconcile(alice, bob)
    assert res.matching_indices == ()
    assert res.discarded_indices == (0, 1, 2)
    assert res.matching_bases == ()
    assert res.total_bits == 3
    assert res.matching_count == 0
    assert res.match_rate == 0.0


@pytest.mark.unit
def test_reconcile_alternating() -> None:
    """Verify reconciliation with alternating match configurations."""
    service = BasisReconciliationService()
    alice = ("Z", "X", "Z", "X")
    bob = ("Z", "Z", "Z", "Z")

    res = service.reconcile(alice, bob)
    assert res.matching_indices == (0, 2)
    assert res.discarded_indices == (1, 3)
    assert res.matching_bases == ("Z", "Z")
    assert res.total_bits == 4
    assert res.matching_count == 2
    assert res.match_rate == 0.5


@pytest.mark.unit
def test_reconcile_invalid_inputs() -> None:
    """Verify validation flags mismatch lengths or invalid basis characters."""
    service = BasisReconciliationService()

    # Mismatch lengths
    with pytest.raises(ValidationError) as exc:
        service.reconcile(("Z", "X"), ("Z",))
    assert "QST-VAL-801" in str(exc.value)

    # Invalid basis values
    with pytest.raises(ValidationError) as exc:
        service.reconcile(("Z", "Y"), ("Z", "X"))
    assert "QST-VAL-602" in str(exc.value)
