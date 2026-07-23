"""Intercept-Resend Eavesdropper wrapper exports.

References:
    Docs/BB84_SPEC.md §5
    Docs/11_SECURITY_ARCHITECTURE.md §3, §4
"""

from qst.core.bb84.eavesdropper import InterceptResendChannel

# Alias for backward compatibility
Eavesdropper = InterceptResendChannel

__all__ = ["InterceptResendChannel", "Eavesdropper"]
