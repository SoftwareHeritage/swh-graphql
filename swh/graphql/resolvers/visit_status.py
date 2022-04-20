from swh.graphql.backends import archive

from .base_connection import BaseConnection
from .base_node import BaseNode


class BaseVisitStatusNode(BaseNode):
    """ """

    @property
    def snapshotId(self):  # To support the schema naming convention
        return self._node.snapshot


class LatestVisitStatusNode(BaseVisitStatusNode):
    """
    Get the latest visit status for a visit
    self.obj is the visit object here
    self.obj.origin is the origin URL
    """

    def _get_node_data(self):
        return archive.Archive().get_latest_visit_status(
            self.obj.origin, self.obj.visitId
        )


class VisitStatusConnection(BaseConnection):
    """
    self.obj is the visit object
    """

    _node_class = BaseVisitStatusNode

    def _get_paged_result(self):
        return archive.Archive().get_visit_status(
            self.obj.origin,
            self.obj.visitId,
            after=self._get_after_arg(),
            first=self._get_first_arg(),
        )
