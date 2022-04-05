"""
"""

from abc import ABC, abstractmethod
from collections import namedtuple


class BaseNode(ABC):
    def __init__(self, obj, info, **kwargs):
        self.obj = obj
        self.info = info
        self.kwargs = kwargs
        node_data = kwargs.get("node_data")
        self._set_node(node_data)

    def _set_node(self, node_data):
        if node_data is None:
            node_data = self._get_node_data()
        self._node = self._get_node_from_data(node_data)

    def _get_node_from_data(self, node_data):
        if type(node_data) is dict:
            return namedtuple("NodeObj", node_data.keys())(*node_data.values())
        return node_data

    def __call__(self, *args, **kw):
        """
        """
        return self

    @abstractmethod
    def _get_node_data(self):
        """
        Override for desired behaviour
        """
        # FIXME, make this call async (not for v1)
        return None

    def __getattr__(self, name):
        """
        Any property defined in the sub-class
        will get precedence over the _node attributes
        """
        return getattr(self._node, name)

    def is_type_of(self):
        return self.__class__.__name__
