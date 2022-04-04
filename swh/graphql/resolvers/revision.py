from swh.graphql.models import RevisionModel

from .base_node import BaseNode


class RevisionNode(BaseNode):
    _model_class = RevisionModel

    def _get_node(self):
        # FIXME, make this call async (not for v1)
        return {"rev": "test"}
