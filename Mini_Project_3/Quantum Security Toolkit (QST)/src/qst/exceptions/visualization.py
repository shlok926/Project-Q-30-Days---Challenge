"""Visualization-specific exception for the Quantum Security Toolkit (QST).

References:
    Docs/10_API_SPECIFICATION.md §6
    Docs/VISUALIZATION_SPEC.md §6
"""

from qst.exceptions.base import QSTError


class VisualizationError(QSTError):
    """Exception raised when rendering or plotting graphs encounters a failure.

    Typical Causes:
        - Missing GUI server/environment for GUI-based matplotlib.
        - Empty or degenerate simulation result properties.
        - Color-blind support palette mapping failures.

    Recommended Handling:
        Re-route to standard text table rendering interfaces, fallback to quiet log mode,
        and log warnings.
    """

    def __init__(self, message: str, code: str = "QST-VIZ-001") -> None:
        """Initialize the visualization error.

        Args:
            message: Details of the rendering error.
            code: Error code registry. Defaults to 'QST-VIZ-001'.
        """
        super().__init__(message, code)
