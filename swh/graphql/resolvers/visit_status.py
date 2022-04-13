from swh.graphql.backends import archive

from .base_connection import BaseConnection
from .base_node import BaseNode


class VisitStatusNode(BaseNode):
    """ """


class VisitStatusConnection(BaseConnection):
    """
    self.obj is the visit object
    """

    _node_class = VisitStatusNode

    def _get_paged_result(self):
        return archive.Archive().get_visit_status(
            self.obj.origin,
            self.obj.visit,
            after=self._get_after_arg(),
            first=self._get_first_arg(),
        )
