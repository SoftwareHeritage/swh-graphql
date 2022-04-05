from swh.graphql.backends import archive
from swh.graphql.utils import utils

from .base_connection import BaseConnection
from .base_node import BaseNode


class VisitStatusNode(BaseNode):
    def _get_node_data(self):
        """
        """

    @property
    def id(self):
        # FIXME, find logic to generate an id
        return utils.encode("dummy-id")


class VisitStatusConnection(BaseConnection):
    """
    self.obj is the visit object
    """

    _node_class = VisitStatusNode

    def _get_page_result(self):
        return archive.Archive().get_visit_status(
            self.obj.origin,
            self.obj.visit,
            after=self._get_after_arg(),
            first=self._get_first_arg(),
        )
