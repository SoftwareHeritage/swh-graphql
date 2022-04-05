from .base_node import BaseNode


class RevisionNode(BaseNode):
    def _get_node_data(self):
        # FIXME, make this call async (not for v1)
        return {"rev": "test"}

    def is_type_of(self):
        return "Revision"
