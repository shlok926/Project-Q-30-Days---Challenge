"""Export-specific exception for the Quantum Security Toolkit (QST).

References:
    Docs/10_API_SPECIFICATION.md §6
    Docs/EXPORT_SPEC.md §4
"""

from qst.exceptions.base import QSTError


class ExportError(QSTError):
    """Exception raised when writing or serialization of simulation results fails.

    Typical Causes:
        - Disk full while exporting research sweeps.
        - Lack of file writing permissions for target directories.
        - Invalid custom serialization codecs.

    Recommended Handling:
        Display file system state feedback, preserving original OS errors
        where applicable, and exit with code 3.
    """

    def __init__(self, message: str, code: str = "QST-EXP-001") -> None:
        """Initialize the export error.

        Args:
            message: Explanation of which file path or schema serialization failed.
            code: Error code registry. Defaults to 'QST-EXP-001'.
        """
        super().__init__(message, code)
