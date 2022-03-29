from abc import ABC


class BaseModel(ABC):
    def __init__(self, node):
        """
        Wrapper class for the swh.model objects
        """
        self._node = node

    def __getattr__(self, name):
        """
        SWH storage is not consistent with
        return types.
        It is returing object in some cases
        and dict in some other
        Fix to handle that inconsistency
        """
        if type(self._node) is dict:
            return self._node.get(name)
        return getattr(self._node, name)
