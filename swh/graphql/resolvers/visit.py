from .base_connection import BaseConnection
from .base_node import BaseNode

from swh.graphql.backends import archive


class OriginVisit(BaseNode):
    def _get_node(self):
        # FIXME, make this call async (not for v1)
        pass


class OriginVisitConnection(BaseConnection):
    def _get_page_results(self):
        # FIXME, make this call async (not for v1)
        return archive.Archive().get_origin_visits(
            self.obj.url, after=self._get_after_arg(), first=self._get_first_arg()
        )
