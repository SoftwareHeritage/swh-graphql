from swh.graphql.backends import archive

from .base_node import BaseNode


class BaseContentNode(BaseNode):
    """ """

    def _get_content_by_id(self, content_id):
        content = archive.Archive().get_content(content_id)
        return content[0] if content else None

    @property
    def id(self):
        return self._node.unique_key()

    @property
    def swhId(self):  # To support the schema naming convention
        return self._node.swhid()

    @property
    def checksum(self):
        # FIXME, return a Node object
        return self._node.hashes()

    @property
    def data(self):
        return

    def is_type_of(self):
        return "Content"


class ContentNode(BaseContentNode):
    def _get_node_data(self):
        """
        When a content is requested directly
        with an id
        """
        return self._get_content_by_id(self.kwargs.get("SWHID").object_id)


class TargetContentNode(BaseContentNode):
    def _get_node_data(self):
        """
        When a content is requested from a
        directory entry or from a release target

        content id is obj.target here
        """
        content_id = self.obj.target
        return self._get_content_by_id(content_id)
