from swh.graphql.backends import archive

from .base_node import BaseNode
from .base_connection import BaseConnection


class SnapshotNode(BaseNode):
    """
    For directly accessing a snapshot with swhid
    """

    def _get_node(self):
        """
        self.obj is visitstatus here
        snapshot swhid is avaialbe in the object
        """
        snapshot_swhid = self.kwargs.get("snapshotId")
        return archive.Archive().get_snapshot(snapshot_swhid)


class VisitSnapshotNode(BaseNode):
    # FIXME, maybe it is a good idea to make a
    # common function for both Node classes
    """
    For accessing a snapshot through the visit type
    """

    def _get_node(self):
        """
        self.obj is visitstatus here
        snapshot swhid is avaialbe in the object
        """
        snapshot_swhid = self.obj.snapshot
        return archive.Archive().get_snapshot(snapshot_swhid)


class SnapshotConnection(BaseConnection):
    pass
