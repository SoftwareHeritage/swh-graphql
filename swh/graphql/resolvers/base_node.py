"""
"""
from abc import ABC, abstractmethod
from typing import Any


class BaseNode(ABC):
    _model_class: Any = None

    def __init__(self, obj, info, **kwargs):
        self.obj = obj
        self.info = info
        self.kwargs = kwargs

        self._node = None

    def __call__(self):
        """
        If a model class is set,
        return its instance, else node as it is
        """
        if self._model_class is not None:
            return self._model_class(self.node)
        return self.node

    @property
    def node(self):
        # This is a small cache to avoid multiple
        # backend calls
        if self._node is None:
            self._node = self._get_node()
        return self._node

    @abstractmethod
    def _get_node(self):
        """
        Override for desired behaviour
        """
        # FIXME, make this call async (not for v1)
        return None
