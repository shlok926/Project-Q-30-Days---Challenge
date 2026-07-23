"""Configuration-specific exception for the Quantum Security Toolkit (QST).

References:
    Docs/10_API_SPECIFICATION.md §6
    Docs/31_CONFIGURATION_REFERENCE.md
"""

from qst.exceptions.base import QSTError


class ConfigurationError(QSTError):
    """Exception raised when configuration loading or parsing fails.

    Typical Causes:
        - Malformed environment variables (e.g. non-numeric inputs for numeric keys).
        - Missing mandatory configuration variables.
        - Non-serializable configuration parameters.

    Recommended Handling:
        Gracefully log the failure and abort program startup, notifying
        the system administrator or user of configuration misalignment.
    """

    def __init__(self, message: str, code: str = "QST-CFG-001") -> None:
        """Initialize the configuration error.

        Args:
            message: Detail on the configuration load failure.
            code: Error code registry. Defaults to 'QST-CFG-001'.
        """
        super().__init__(message, code)
