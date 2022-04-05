from swh.graphql.backends import archive
from swh.graphql.utils import utils

from .base_node import BaseNode


class SnapshotNode(BaseNode):
    """
    For directly accessing a snapshot with swhid
    """

    def _get_node_data(self):
        """
        """
        # FIXME, use methods from SWH core
        snapshot_swhid = utils.str_to_swid(self.kwargs.get("SWHId"))
        return archive.Archive().get_snapshot(snapshot_swhid)


class VisitSnapshotNode(BaseNode):
    # FIXME, maybe it is a good idea to make a
    # common function for both Node classes (for handling exceptions)
    """
    For accessing a snapshot from a visitstatus type
    """
    node_class = SnapshotNode

    def _get_node_data(self):
        """
        self.obj is visitstatus here
        snapshot swhid is avaialbe in the parent (self.obj)
        """
        return archive.Archive().get_snapshot(self.obj.snapshot)


# class SnapshotConnection(BaseConnection):
#     """
#     To get all the snapshots under an origin
#     """

#     _node_class = SnapshotNode
