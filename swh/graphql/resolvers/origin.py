from swh.graphql.backends import archive

from .base_connection import BaseConnection
from .base_node import BaseNode


class OriginNode(BaseNode):
    def _get_node_data(self):
        return archive.Archive().get_origin(self.kwargs.get("url"))


class OriginConnection(BaseConnection):
    _node_class = OriginNode

    def _get_paged_result(self):
        search_pattern = self.kwargs.get("urlPattern")
        # STORAGE-TODO
        # Make them a single function in the backend
        if search_pattern:
            return archive.Archive().search_origins(
                pattern=self.kwargs.get("urlPattern"),
                after=self._get_after_arg(),
                first=self._get_first_arg(),
            )
        else:
            return archive.Archive().get_origins(
                after=self._get_after_arg(),
                first=self._get_first_arg(),
            )
