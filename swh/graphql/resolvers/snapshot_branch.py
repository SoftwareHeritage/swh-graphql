# from swh.graphql.backends import archive
from swh.graphql.models import SnapshotBranchModel

# from swh.graphql.utils import utils
from swh.storage.interface import PagedResult

from .base_connection import BaseConnection


class SnapshotBranchConnection(BaseConnection):
    _model_class = SnapshotBranchModel

    def _get_page_result(self):
        # FIXME making extra query to the storage
        # This is failing now (STORAGEFIX)
        # This is not really needed as we have the data
        # in the self.obj itself
        # Mocking paged data
        # result = archive.Archive().get_snapshot_branches(
        # utils.str_to_swid(self.obj.id.hex()),
        # after=self._get_after_arg(),
        # first=self._get_first_arg())
        # return PagedResult(results=result['branches'],
        #                    next_page_token=result['next_branch'])
        return self._get_from_parent_node()

    def _get_from_parent_node(self):
        """
        Branches are avaialble in the snapshot object itself
        Not making a query
        """
        results = [
            {"name": key, "type": value["target_type"], "id": "temp-id"}
            for (key, value) in self.obj.branches.items()
        ]
        # FIXME, this pagination is broken, fix it with swh-storage
        return PagedResult(results=results, next_page_token=self.obj.next_branch)

    def total_count(self):
        return None
