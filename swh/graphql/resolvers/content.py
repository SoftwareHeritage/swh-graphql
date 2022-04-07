from swh.graphql.backends import archive
from swh.graphql.utils import utils

from .base_node import BaseNode


class BaseContentNode(BaseNode):
    def _get_content_by_id(self, content_id):
        return archive.Archive().get_content(content_id)

    @property
    def id(self):
        return b"test"


class ContentNode(BaseContentNode):
    def _get_node_data(self):
        """
        When a content is requested directly
        (not from a connection) with an id
        """
        content_id = utils.str_to_swid(self.kwargs.get("SWHId"))
        return self._get_content_by_id(content_id)[0]
