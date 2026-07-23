"""Simulation-specific exception for the Quantum Security Toolkit (QST).

References:
    Docs/10_API_SPECIFICATION.md §6, §7
    Docs/07_SYSTEM_ARCHITECTURE.md §11
"""

from qst.exceptions.base import QSTError


class SimulationError(QSTError):
    """Exception raised when the underlying quantum simulator encounters a failure.

    Typical Causes:
        - Qiskit Aer backend crashes or encounters out-of-memory states.
        - Invalid circuit compilation.
        - Disconnection or failure when querying backends.

    Recommended Handling:
        Catch and encapsulate low-level simulator errors, ensuring
        raw stack traces of external libraries (like Qiskit) are wrapped,
        and log using debug mode while exiting with code 2.
    """

    def __init__(self, message: str, code: str = "QST-SIM-001") -> None:
        """Initialize the simulation error.

        Args:
            message: Details of the backend simulation failure.
            code: Error code registry. Defaults to 'QST-SIM-001'.
        """
        super().__init__(message, code)
