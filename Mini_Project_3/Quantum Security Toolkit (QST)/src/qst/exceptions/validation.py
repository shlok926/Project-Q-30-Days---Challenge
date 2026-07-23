"""Validation-specific exception for the Quantum Security Toolkit (QST).

References:
    Docs/10_API_SPECIFICATION.md §6
    Docs/05_PRODUCT_REQUIREMENTS.md §7
"""

from qst.exceptions.base import QSTError


class ValidationError(QSTError):
    """Exception raised when input parameters fail verification.

    Typical Causes:
        - Non-positive or non-integer qubit counts (e.g. n_qubits <= 0).
        - Interception probability outside the [0.0, 1.0] range.
        - Non-integer seeds.
        - Non-existent or non-writable paths.

    Recommended Handling:
        Catch at user-interaction boundaries (e.g., CLI or web routing)
        and present the error message clearly, exiting with code 1.
    """

    def __init__(self, message: str, code: str = "QST-VAL-001") -> None:
        """Initialize the validation error.

        Args:
            message: Explanation of which parameters were invalid.
            code: Error code registry. Defaults to 'QST-VAL-001'.
        """
        super().__init__(message, code)
