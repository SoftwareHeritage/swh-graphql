from abc import ABC
from collections import namedtuple

from swh.graphql.errors import ObjectNotFoundError


class BaseNode(ABC):
    """
    Base class for all the Node resolvers
    """

    def __init__(self, obj, info, node_data=None, **kwargs):
        self.obj = obj
        self.info = info
        self.kwargs = kwargs
        self._set_node(node_data)

    def _set_node(self, node_data):
        if node_data is None:
            node_data = self._get_node_data()
        self._node = self._get_node_from_data(node_data)

    def _get_node_from_data(self, node_data):
        """
        Create an object from the dict
        Override to support complex data structures
        """
        if node_data is None:
            self._handle_none_data()

        if type(node_data) is dict:
            return namedtuple("NodeObj", node_data.keys())(*node_data.values())
        return node_data

    def _handle_none_data(self):
        """
        raise and error in case the object returned is None
        override for desired behaviour
        """
        raise ObjectNotFoundError("Requested object is not available")

    def __call__(self, *args, **kw):
        return self

    def _get_node_data(self):
        """
        Override for desired behaviour
        This will be called only when
        node_data is not available
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
