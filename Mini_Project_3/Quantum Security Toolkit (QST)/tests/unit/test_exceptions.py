"""Unit tests for QST exception classes.

References:
    Docs/10_API_SPECIFICATION.md §6
    Docs/14_TESTING_STRATEGY.md §3
"""

import pytest

from qst.exceptions.base import QSTError
from qst.exceptions.validation import ValidationError


@pytest.mark.unit
def test_qst_error_string_representation() -> None:
    """Verify QSTError displays custom codes and messages in string representation."""
    err = QSTError("A generic error occurred", code="QST-ERR-999")
    assert str(err) == "[QST-ERR-999] A generic error occurred"
    assert err.code == "QST-ERR-999"
    assert err.message == "A generic error occurred"


@pytest.mark.unit
def test_validation_error_subclass() -> None:
    """Verify ValidationError inherits from QSTError and formats defaults correctly."""
    err = ValidationError("Qubit size out of bounds")
    assert isinstance(err, QSTError)
    assert err.code == "QST-VAL-001"
    assert str(err) == "[QST-VAL-001] Qubit size out of bounds"
