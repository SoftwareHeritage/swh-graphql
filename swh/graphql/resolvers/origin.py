from swh.graphql.backends import archive

from .base_connection import BaseConnection
from .base_model import BaseModel
from .base_node import BaseNode


class OriginModel(BaseModel):
    pass


class OriginNode(BaseNode):
    _model_class = OriginModel

    def _get_node(self):
        # FIXME, make this call async (not for v1)
        return archive.Archive().get_origin(self.kwargs.get("url"))


class OriginConnection(BaseConnection):
    _model_class = OriginModel

    def _get_page_result(self):
        # FIXME, make this call async (not for v1)
        return archive.Archive().get_origins(
            after=self._get_after_arg(), first=self._get_first_arg()
        )
