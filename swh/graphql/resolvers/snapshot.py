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
    For directly accessing a snapshot with an Id
    """

    def _get_node_data(self):
        """ """
        snapshot_id = utils.str_to_sha1(self.kwargs.get("Sha1"))
        return self._get_snapshot_by_id(snapshot_id)


class VisitSnapshotNode(BaseSnapshotNode):
    """
    For accessing a snapshot from a visitstatus type
    """

    def _get_node_data(self):
        """
        self.obj is visitstatus here
        self.obj.snapshot is the requested snapshot id
        """
        return self._get_snapshot_by_id(self.obj.snapshot)
