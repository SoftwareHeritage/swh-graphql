from swh.graphql.models import ReleaseModel

from .base_node import BaseNode


class ReleaseNode(BaseNode):
    _model_class = ReleaseModel

    def _get_node(self):
        # FIXME, make this call async (not for v1)
        return {"rel": "test"}
