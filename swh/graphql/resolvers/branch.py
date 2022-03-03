# from swh.graphql.backends import archive

from .base_connection import BaseConnection


class SnapshotBranchConnection(BaseConnection):
    def _get_page_result(self):
        """
        Branches are avaialble in the snapshot object itself
        Not making a query
        """

        return self.obj["branches"]

        # return archive.Archive().get_snapshot_branches(
        #     after=self._get_after_arg(), first=self._get_first_arg()
        # )
