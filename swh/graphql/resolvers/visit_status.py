from swh.graphql.backends import archive
from swh.graphql.utils import utils

from .base_connection import BaseConnection
from .base_model import BaseModel


class VisitStatusModel(BaseModel):
    @property
    def id(self):
        # FIXME
        return utils.encode("temp-id")


class VisitStatusConnection(BaseConnection):
    _model_class = VisitStatusModel

    def _get_page_result(self):
        return archive.Archive().get_visit_status(
            self.obj.origin,
            self.obj.visit,
            after=self._get_after_arg(),
            first=self._get_first_arg(),
        )
