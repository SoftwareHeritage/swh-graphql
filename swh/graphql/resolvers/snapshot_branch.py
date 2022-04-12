from collections import namedtuple

from swh.graphql.backends import archive
from swh.graphql.utils import utils
from swh.storage.interface import PagedResult

from .base_connection import BaseConnection
from .base_node import BaseNode


class SnapshotBranchNode(BaseNode):
    """
    target field for this Node is a UNION in the schema
    It is resolved in resolvers.resolvers.py
    """

    def _get_node_from_data(self, node_data):
        """
        node_data is not a dict in this case
        overriding to support this special data structure
        """

        branch_name, branch_obj = node_data
        node = {
            "name": branch_name,
            "type": branch_obj.target_type.value,
            "target": branch_obj.target,
        }
        return namedtuple("NodeObj", node.keys())(*node.values())


class SnapshotBranchConnection(BaseConnection):
    _node_class = SnapshotBranchNode

    def _get_paged_result(self):
        """
        When branches requested from a snapshot
        self.obj.id is snapshot_id here
        (as returned from resolvers/snapshot.py)
        """

        # FIXME, this pagination is not consistent with other connections
        # FIX in swh-storage to return PagedResult
        result = archive.Archive().get_snapshot_branches(
            self.obj.id, after=self._get_after_arg(), first=self._get_first_arg()
        )
        # FIXME Cursor must be a hex to be consistent with
        # the base class, hack to make that work
        end_cusrsor = (
            result["next_branch"].hex() if result["next_branch"] is not None else None
        )
        return PagedResult(
            results=result["branches"].items(), next_page_token=end_cusrsor
        )

    def _get_after_arg(self):
        """
        Snapshot branch is using a different cursor; logic to handle that
        """
        # FIXME Cursor must be a hex to be consistent with
        # the base class, hack to make that work
        after = utils.get_decoded_cursor(self.kwargs.get("after", ""))
        return bytes.fromhex(after)
