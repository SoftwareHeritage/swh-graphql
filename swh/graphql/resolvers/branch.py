# from swh.graphql.backends import archive
from swh.storage.interface import PagedResult

from .base_connection import BaseConnection


class SnapshotBranchConnection(BaseConnection):
    def _get_page_result(self):
        """
        Branches are avaialble in the snapshot object itself
        Not making a query
        """
        # FIXME Mocking PagedResult to make base_connection work
        # Fix this in swh-storage
        results = [
            {"name": key, "type": value["target_type"]}
            for (key, value) in self.obj["branches"].items()
        ]
        # FIXME, this pagination is broken, fix it with swh-storage
        return PagedResult(results=results, next_page_token=self.obj["next_branch"])
