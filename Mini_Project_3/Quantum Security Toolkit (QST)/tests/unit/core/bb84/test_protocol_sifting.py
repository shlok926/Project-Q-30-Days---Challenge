"""Unit tests verifying the integrated BB84 Protocol execution with basis reconciliation and sifting.

References:
    Docs/BB84_SPEC.md §1
    Docs/10_API_SPECIFICATION.md §5
    Docs/14_TESTING_STRATEGY.md §3
"""

import pytest

from qst.core.bb84.protocol import BB84Protocol
from qst.models.results import SimulationResult


@pytest.mark.unit
def test_bb84_protocol_sifting_integration() -> None:
    """Verify BB84Protocol completes basis reconciliation and key sifting on run."""
    protocol = BB84Protocol()

    # 1. Initialize
    protocol.initialize(n_qubits=20, seed=123)

    # 2. Execute state prep
    protocol.execute()

    # 3. Measure Bob & run reconciliation + sifting
    protocol.measure()

    # Verify reconciliation result is populated on protocol
    recon = protocol.reconciliation
    assert recon is not None
    assert recon.total_bits == 20
    assert recon.matching_count == len(recon.matching_indices)

    # Verify sifted keys are populated on protocol
    sifted = protocol.sifted_keys
    assert sifted is not None
    assert sifted.key_length == len(sifted.alice_key)
    assert len(sifted.alice_key) == recon.matching_count

    # 4. Export result
    result = protocol.export()
    assert isinstance(result, SimulationResult)

    # Verify fields in SimulationResult
    assert result.final_key_length == sifted.key_length
    assert result.key_rate == float(sifted.key_length / 20)
    assert result.sifted_key == list(sifted.alice_key)
    assert result.alice_bits == protocol.alice_bits
    assert result.bob_bits == protocol.bob_bits
    assert result.alice_bases == protocol.alice_bases
    assert result.bob_bases == protocol.bob_bases
    assert result.reconciliation == recon
    assert result.sifted_keys == sifted

    # Verify that the internal circuit is not present in SimulationResult attributes
    assert not hasattr(result, "prepared_circuit")
    assert not hasattr(result, "measured_circuit")

    # In a noise-free simulation, Alice's key and Bob's key must match perfectly!
    assert sifted.alice_key == sifted.bob_key
