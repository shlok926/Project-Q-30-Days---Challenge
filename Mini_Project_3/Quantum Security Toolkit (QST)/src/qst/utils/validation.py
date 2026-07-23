"""Reusable validation utilities for input parameters.

References:
    Docs/05_PRODUCT_REQUIREMENTS.md §7, §11
    Docs/10_API_SPECIFICATION.md §6
"""

from pathlib import Path
from typing import Any, Optional

from qst.exceptions.validation import ValidationError


def validate_qubit_count(value: Any) -> int:
    """Validate that the qubit count is a positive integer.

    Args:
        value: Input value to validate.

    Returns:
        The validated qubit count as an integer.

    Raises:
        ValidationError: If qubit count is <= 0 or not an integer.
    """
    if not isinstance(value, int) or isinstance(value, bool):
        raise ValidationError(
            f"Qubit count must be an integer, got {type(value).__name__}",
            code="QST-VAL-101",
        )
    if value <= 0:
        raise ValidationError(
            f"Qubit count must be a positive integer, got {value}",
            code="QST-VAL-102",
        )
    return value


def validate_probability(value: Any, name: str = "Probability") -> float:
    """Validate that a probability value is a float between 0.0 and 1.0.

    Args:
        value: Input value to validate.
        name: Name of the variable being validated (for error reporting).

    Returns:
        The validated probability as a float.

    Raises:
        ValidationError: If probability is not a float or outside [0.0, 1.0].
    """
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        raise ValidationError(
            f"{name} must be a numeric value, got {type(value).__name__}",
            code="QST-VAL-201",
        )
    val_float = float(value)
    if not (0.0 <= val_float <= 1.0):
        raise ValidationError(
            f"{name} must be between 0.0 and 1.0, got {value}",
            code="QST-VAL-202",
        )
    return val_float


def validate_seed(value: Any) -> Optional[int]:
    """Validate that the seed is a valid optional integer.

    Args:
        value: Input value to validate.

    Returns:
        The validated seed (int or None).

    Raises:
        ValidationError: If seed is not an integer and not None.
    """
    if value is None:
        return None
    if not isinstance(value, int) or isinstance(value, bool):
        raise ValidationError(
            f"Seed must be an integer or None, got {type(value).__name__}",
            code="QST-VAL-301",
        )
    return value


def validate_output_directory(value: Any) -> Path:
    """Validate that the output directory exists or can be created.

    Args:
        value: The path input to validate.

    Returns:
        The validated Path object.

    Raises:
        ValidationError: If directory cannot be created or is not writable.
    """
    if not isinstance(value, (str, Path)):
        raise ValidationError(
            f"Output directory must be a path or string, got {type(value).__name__}",
            code="QST-VAL-401",
        )
    path = Path(value)
    try:
        if not path.exists():
            path.mkdir(parents=True, exist_ok=True)
        # Test write permissions by creating a temporary directory check
        test_file = path / ".qst_write_test"
        test_file.touch()
        test_file.unlink()
    except (OSError, PermissionError) as e:
        raise ValidationError(
            f"Output directory '{value}' is not writable or cannot be created. Reason: {e}",
            code="QST-VAL-402",
        ) from e
    return path
