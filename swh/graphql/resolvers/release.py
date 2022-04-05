from .base_node import BaseNode


class ReleaseNode(BaseNode):
    def _get_node_data(self):
        # FIXME, make this call async (not for v1)
        return {"rel": "test"}

    def is_type_of(self):
        return "Release"
