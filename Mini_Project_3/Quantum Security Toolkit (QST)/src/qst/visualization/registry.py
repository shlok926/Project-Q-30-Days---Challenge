"""Registry for managing plotting visualization backends.

References:
    Docs/VISUALIZATION_SPEC.md §3
    Docs/07_SYSTEM_ARCHITECTURE.md §11
"""

from typing import Dict, Type
from qst.visualization.backend import VisualizationBackend


class VisualizationBackendRegistry:
    """Registry class managing pluggable visualization backend classes."""

    _registry: Dict[str, Type[VisualizationBackend]] = {}

    @classmethod
    def register(cls, name: str, backend_class: Type[VisualizationBackend]) -> None:
        """Register a backend class under a unique name.

        Args:
            name: String identifier (e.g. 'matplotlib').
            backend_class: Subclass of VisualizationBackend.
        """
        cls._registry[name.lower()] = backend_class

    @classmethod
    def get(cls, name: str, *args, **kwargs) -> VisualizationBackend:
        """Instantiate and return the requested backend.

        Args:
            name: String identifier of the backend.
            *args: Positional arguments for backend constructor.
            **kwargs: Keyword arguments for backend constructor.

        Returns:
            An instance of VisualizationBackend.

        Raises:
            KeyError: If name is not registered.
        """
        key = name.lower()
        if key not in cls._registry:
            raise KeyError(f"Backend '{name}' is not registered.")
        return cls._registry[key](*args, **kwargs)


# Pre-register default Matplotlib backend
from qst.visualization.matplotlib_backend import MatplotlibBackend

VisualizationBackendRegistry.register("matplotlib", MatplotlibBackend)
