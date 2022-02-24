from .base_connection import BaseConnection

from swh.graphql.backends import archive


class OriginVisitConnection(BaseConnection):
    def _get_page_results(self):
        return archive.Archive().get_origin_visits(
            self.obj.url, after=self.kwargs.get("after"), first=self.kwargs.get("first")
        )
