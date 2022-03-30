from swh.graphql.backends import archive
from swh.graphql.models import VisitStatusModel

from .base_connection import BaseConnection


class VisitStatusConnection(BaseConnection):
    _model_class = VisitStatusModel

    def _get_page_result(self):
        return archive.Archive().get_visit_status(
            self.obj.origin,
            self.obj.visit,
            after=self._get_after_arg(),
            first=self._get_first_arg(),
        )
