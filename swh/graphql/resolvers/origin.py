from .base_connection import BaseConnection
from .base_node import BaseNode

from swh.graphql.backends import archive


class OriginConnection(BaseConnection):
    def _get_page_results(self):
        # FIXME, make this call async (not for v1)
        return archive.Archive().get_origins(
            after=self.kwargs.get("after"), first=self.kwargs.get("first", 50)
        )


class OriginNode(BaseNode):
    def _get_node(self):
        # FIXME, make this call async (not for v1)
        return archive.Archive().get_origin(self.kwargs.get("url"))
