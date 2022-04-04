from abc import ABC
from collections import namedtuple


class BaseModel(ABC):
    def __init__(self, node):
        """
        Wrapper class for the model objects

        SWH storage is not consistent with
        return types.
        It is returing object in some cases
        and dict in some other
        Mocking an object in case of dict
        """
        # FIXME, this could fail in nested dicts
        if type(node) is dict:
            self._node = namedtuple("ModelObj", node.keys())(*node.values())
        else:
            self._node = node

    def __getattr__(self, name):
        """
        Any property defined in the sub-class
        will get precedence over the _node attributes
        """
        return getattr(self._node, name)

    def is_type_of(self):
        return self.__class__.__name__
