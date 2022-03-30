from swh.graphql.backends import archive
from swh.graphql.utils import utils

from .base_connection import BaseConnection
from .base_model import BaseModel
from .base_node import BaseNode


class VisitModel(BaseModel):
    @property
    def id(self):
        # FIXME
        return utils.encode(f"{self.origin}-{str(self.visit)}")


class OriginVisitNode(BaseNode):
    _model_class = VisitModel

    def _get_node(self):
        # FIXME, make this call async (not for v1)
        return archive.Archive().get_origin_visit(
            self.kwargs.get("originUrl"), int(self.kwargs.get("id"))
        )


class OriginVisitConnection(BaseConnection):
    _model_class = VisitModel

    def _get_page_result(self):
        """
        Get the visits for the given origin
        parent obj (self.obj) is origin here
        """
        # FIXME, make this call async (not for v1)
        return archive.Archive().get_origin_visits(
            self.obj.url, after=self._get_after_arg(), first=self._get_first_arg()
        )
