# from swh.graphql.backends import archive
# from swh.graphql.utils import utils
from swh.storage.interface import PagedResult

from .base_connection import BaseConnection
from .base_node import BaseNode


class SnapshotBranchNode(BaseNode):
    """
    """

    def _get_node_data(self):
        """
        This Node is instantiated only from a
        connection (SnapshotBranchConnection).
        Since node_data is always available,
        there is no reason to make a storage
        query. Hence this function will never
        be called. This stub is to make the
        abstract base class work.
        """


class SnapshotBranchConnection(BaseConnection):
    _node_class = SnapshotBranchNode

    def _get_paged_result(self):
        return self._get_from_parent_node()

        # FIXME making extra query to the storage
        # This is not really needed as we have the data
        # in the self.obj itself
        # Mocking paged data
        # result = archive.Archive().get_snapshot_branches(
        #     utils.str_to_swid(self.obj.id.hex()),
        #     after=self._get_after_arg(),
        #     first=self._get_first_arg())
        # return PagedResult(results=result['branches'],
        #                    next_page_token=result['next_branch'].hex())

    def _get_from_parent_node(self):
        """
        Branches are avaialble in the snapshot object itself
        Not making an extra query
        """

        results = [
            {
                "name": key,
                "type": value["target_type"],
                "id": "temp-id",
                "target": value["target"],
            }
            for (key, value) in self.obj.branches.items()
        ][: self._get_first_arg()]
        # FIXME, this pagination is broken, fix it with swh-storage
        # Mocking PagedResult obj
        return PagedResult(results=results, next_page_token=self.obj.next_branch)

    def total_count(self):
        # FIXME, this can be implemented with current swh.storage API
        return None
