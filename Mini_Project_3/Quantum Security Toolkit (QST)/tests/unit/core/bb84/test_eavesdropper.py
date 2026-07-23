"""Unit tests for the BB84 InterceptResendChannel eavesdropper implementation.

References:
    Docs/BB84_SPEC.md §5
    Docs/14_TESTING_STRATEGY.md §3
"""

import pytest

from qst.core.bb84.eavesdropper import InterceptResendChannel
from qst.core.shared.random.random_provider import NumpyRandomProvider
from qst.exceptions.validation import ValidationError
from qst.models.results import EveSimulationResult


@pytest.mark.unit
def test_eavesdropper_no_attack() -> None:
    """Verify that interception_probability=0.0 results in zero interceptions."""
    rand = NumpyRandomProvider(seed=42)
    channel = InterceptResendChannel(rand)

    alice_bits = (1, 0, 1, 0, 1)
    alice_bases = ("Z", "X", "Z", "X", "Z")

    res = channel.intercept_and_resend(alice_bits, alice_bases, 0.0)
    assert isinstance(res, EveSimulationResult)
    assert not any(res.intercepted_mask)
    assert res.eve_bases == ("", "", "", "", "")
    assert res.eve_measurements == (None, None, None, None, None)
    assert res.reconstructed_bits == alice_bits
    assert res.reconstructed_bases == alice_bases


@pytest.mark.unit
def test_eavesdropper_full_attack() -> None:
    """Verify that interception_probability=1.0 intercepts all qubits."""
    rand = NumpyRandomProvider(seed=42)
    channel = InterceptResendChannel(rand)

    alice_bits = (1, 0, 1, 0, 1)
    alice_bases = ("Z", "X", "Z", "X", "Z")

    res = channel.intercept_and_resend(alice_bits, alice_bases, 1.0)
    assert all(res.intercepted_mask)
    assert all(b in ("Z", "X") for b in res.eve_bases)
    assert all(m in (0, 1) for m in res.eve_measurements)
    assert len(res.reconstructed_bits) == 5
    assert len(res.reconstructed_bases) == 5


@pytest.mark.unit
def test_eavesdropper_partial_attack() -> None:
    """Verify partial attack selects some but not all qubits."""
    rand = NumpyRandomProvider(seed=123)
    channel = InterceptResendChannel(rand)

    alice_bits = (1,) * 20
    alice_bases = ("Z",) * 20

    res = channel.intercept_and_resend(alice_bits, alice_bases, 0.5)
    # At probability 0.5, some should be intercepted, some not
    assert any(res.intercepted_mask)
    assert not all(res.intercepted_mask)


@pytest.mark.unit
def test_eavesdropper_determinism() -> None:
    """Verify that fixed seed yields identical attack parameters and outcomes."""
    rand1 = NumpyRandomProvider(seed=777)
    channel1 = InterceptResendChannel(rand1)

    rand2 = NumpyRandomProvider(seed=777)
    channel2 = InterceptResendChannel(rand2)

    alice_bits = (1, 0, 1, 1, 0, 1, 0, 0, 1, 0)
    alice_bases = ("Z", "X", "Z", "X", "Z", "X", "Z", "X", "Z", "X")

    res1 = channel1.intercept_and_resend(alice_bits, alice_bases, 0.4)
    res2 = channel2.intercept_and_resend(alice_bits, alice_bases, 0.4)

    assert res1.intercepted_mask == res2.intercepted_mask
    assert res1.eve_bases == res2.eve_bases
    assert res1.eve_measurements == res2.eve_measurements
    assert res1.reconstructed_bits == res2.reconstructed_bits
    assert res1.reconstructed_bases == res2.reconstructed_bases


@pytest.mark.unit
def test_eavesdropper_validation_failures() -> None:
    """Verify validation checks trigger on invalid input lengths or probabilities."""
    rand = NumpyRandomProvider(seed=42)
    channel = InterceptResendChannel(rand)

    # Out of bounds probability
    with pytest.raises(ValidationError) as exc:
        channel.intercept_and_resend((1, 0), ("Z", "X"), 1.5)
    assert "QST-VAL-202" in str(exc.value)

    # Mismatched bits and bases lengths
    with pytest.raises(ValidationError) as exc:
        channel.intercept_and_resend((1, 0), ("Z",), 0.5)
    assert "QST-VAL-804" in str(exc.value)


@pytest.mark.unit
def test_eve_simulation_result_post_init() -> None:
    """Verify EveSimulationResult validates identical length of its collections."""
    with pytest.raises(ValidationError) as exc:
        EveSimulationResult(
            intercepted_mask=(True, False),
            eve_bases=("Z",),
            eve_measurements=(1, None),
            reconstructed_bits=(1, 0),
            reconstructed_bases=("Z", "X"),
        )
    assert "QST-VAL-514" in str(exc.value)
