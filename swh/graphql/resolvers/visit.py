from swh.graphql.backends import archive

from .base_connection import BaseConnection
from .base_node import BaseNode


class OriginVisit(BaseNode):
    def _get_node(self):
        # FIXME, make this call async (not for v1)
        return archive.Archive().get_origin_visit(
            self.kwargs.get("originUrl"), int(self.kwargs.get("id"))
        )


class OriginVisitConnection(BaseConnection):
    def _get_page_result(self):
        """
        Get the visits for the given origin
        parent obj (self.obj) is origin here
        """
        # FIXME, make this call async (not for v1)
        return archive.Archive().get_origin_visits(
            self.obj.url, after=self._get_after_arg(), first=self._get_first_arg()
        )


class VisitStatusConnection(BaseConnection):
    def _get_page_result(self):
        s = archive.Archive().get_visit_status(
            self.obj.origin,
            self.obj.visit,
            after=self._get_after_arg(),
            first=self._get_first_arg(),
        )
        return s
