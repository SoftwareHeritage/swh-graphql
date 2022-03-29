# from swh.graphql.backends import archive
from swh.storage.interface import PagedResult

from .base_connection import BaseConnection
from .base_model import BaseModel


class BranchModel(BaseModel):
    pass


class SnapshotBranchConnection(BaseConnection):
    _model_class = BranchModel

    def _get_page_result(self):
        """
        Branches are avaialble in the snapshot object itself
        Not making a query
        """
        # FIXME Mocking PagedResult to make base_connection work
        # FIX this in swh-storage
        # FIX id
        import pdb

        pdb.set_trace()
        results = [
            {"name": key, "type": value["target_type"], "id": "temp-id"}
            for (key, value) in self.obj.branches.items()
        ][:5]
        # FIXME, this pagination is broken, fix it with swh-storage
        return PagedResult(results=results, next_page_token=self.obj["next_branch"])
