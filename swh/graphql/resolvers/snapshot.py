from swh.graphql.utils import utils

from .base_node import BaseNode


class BaseSnapshotNode(BaseNode):
    def _get_snapshot_by_id(self, snapshot_id):
        # Now not fetching any data (schema is exposing just id)
        # same pattern is used in directory resolver
        return {
            "id": snapshot_id,
        }


class SnapshotNode(BaseSnapshotNode):
    """
    For directly accessing a snapshot with swhid
    """

    def _get_node_data(self):
        """ """
        # FIXME, use methods from SWH core
        snapshot_id = utils.str_to_swid(self.kwargs.get("Sha1"))
        return self._get_snapshot_by_id(snapshot_id)


class VisitSnapshotNode(BaseSnapshotNode):
    """
    For accessing a snapshot from a visitstatus type
    """

    def _get_node_data(self):
        """
        self.obj is visitstatus here
        snapshot sha1 is available in the visit object (self.obj)
        """
        return self._get_snapshot_by_id(self.obj.snapshot)


# class SnapshotConnection(BaseConnection):
#     """
#     To get all the snapshots under an origin
#     """

#     _node_class = SnapshotNode
