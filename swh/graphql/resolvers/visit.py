from swh.graphql.backends import archive
from swh.graphql.utils import utils

from .base_connection import BaseConnection
from .base_node import BaseNode


class OriginVisitNode(BaseNode):
    def _get_node_data(self):
        # FIXME, make this call async (not for v1)
        return archive.Archive().get_origin_visit(
            self.kwargs.get("originUrl"), int(self.kwargs.get("id"))
        )

    @property
    def id(self):
        # FIXME, use a better id
        return utils.encode(f"{self.origin}-{str(self.visit)}")


class OriginVisitConnection(BaseConnection):
    _node_class = OriginVisitNode

    def _get_paged_result(self):
        """
        Get the visits for the given origin
        parent obj (self.obj) is origin here
        """
        # FIXME, make this call async (not for v1)
        return archive.Archive().get_origin_visits(
            self.obj.url, after=self._get_after_arg(), first=self._get_first_arg()
        )
