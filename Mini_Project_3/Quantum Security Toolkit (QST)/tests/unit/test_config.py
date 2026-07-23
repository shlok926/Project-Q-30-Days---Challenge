"""Unit tests for the QST configuration layer.

References:
    Docs/31_CONFIGURATION_REFERENCE.md
    Docs/14_TESTING_STRATEGY.md §3
"""

import os
from unittest import mock

import pytest

from qst.config.settings import QST_VERSION, Configuration
from qst.exceptions.configuration import ConfigurationError


@pytest.mark.unit
def test_default_configuration() -> None:
    """Verify default configurations are loaded correctly when env is empty."""
    with mock.patch.dict(os.environ, {}, clear=True):
        config = Configuration()
        assert config.log_level == "INFO"
        assert config.version == QST_VERSION


@pytest.mark.unit
def test_custom_log_level() -> None:
    """Verify Configuration parses custom valid QST_LOG_LEVEL correctly."""
    with mock.patch.dict(os.environ, {"QST_LOG_LEVEL": "debug"}):
        config = Configuration()
        assert config.log_level == "DEBUG"


@pytest.mark.unit
def test_invalid_log_level() -> None:
    """Verify Configuration raises ConfigurationError on unrecognized log level."""
    with mock.patch.dict(os.environ, {"QST_LOG_LEVEL": "invalid_level"}):
        with pytest.raises(ConfigurationError) as exc_info:
            Configuration()
        assert "QST-CFG-101" in str(exc_info.value)
        assert "INVALID_LEVEL" in str(exc_info.value)
