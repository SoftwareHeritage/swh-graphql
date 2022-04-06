from swh.graphql.backends import archive

from .base_connection import BaseConnection
from .base_node import BaseNode


class OriginNode(BaseNode):
    def _get_node_data(self):
        # FIXME, make this call async (not for v1)
        return archive.Archive().get_origin(self.kwargs.get("url"))

    # @property
    # def url(self):
    #     return "test"


class OriginConnection(BaseConnection):
    _node_class = OriginNode

    def _get_paged_result(self):
        # FIXME, make this call async (not for v1)
        return archive.Archive().get_origins(
            after=self._get_after_arg(), first=self._get_first_arg()
        )
