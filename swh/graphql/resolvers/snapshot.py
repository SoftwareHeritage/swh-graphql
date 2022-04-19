from swh.graphql.backends import archive
from swh.graphql.utils import utils

from .base_connection import BaseConnection
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


class OriginSnapshotConnection(BaseConnection):
    _node_class = BaseSnapshotNode

    def _get_paged_result(self):
        """ """
        results = archive.Archive().get_origin_snapshots(self.obj.url)
        snapshots = [{"id": snapshot} for snapshot in results]
        # FIXME, using dummy(local) pagination, move pagination to backend
        # To remove localpagination, just drop the paginated call
        # STORAGE-TODO
        return utils.paginated(snapshots, self._get_first_arg(), self._get_after_arg())
