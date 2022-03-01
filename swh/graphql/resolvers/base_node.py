"""
"""


class BaseNode:
    def __init__(self, obj, info, **kwargs):
        self.obj = obj
        self.info = info
        self.kwargs = kwargs

        self._node = None

    def __call__(self):
        return self.node

    @property
    def node(self):
        if self._node is None:
            self._node = self._get_node()
        return self._node

    def _get_node(self):
        """
        Override for desired behaviour
        """

        return None
