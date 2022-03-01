"""
"""
from abc import ABC, abstractmethod


class BaseNode(ABC):
    def __init__(self, obj, info, **kwargs):
        self.obj = obj
        self.info = info
        self.kwargs = kwargs

        self._node = None

    def __call__(self):
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

        return None
