from swh.graphql.backends import archive
from swh.graphql.utils import utils

from .base_node import BaseNode


class BaseDirectoryNode(BaseNode):
    def _get_directory_by_id(self, directory_id):
        return archive.Archive().get_directory(directory_id)

    @property
    def entries(self):
        # FIXME, return a paginated list of
        # directory or contnet node object
        return self._node[0]["name"]

    @property
    def name(self):
        return b"test-name"

    @property
    def id(self):
        return b"test-id"


class DirectoryNode(BaseDirectoryNode):
    def _get_node_data(self):
        """
        When a directory is requested directly
        (not from a connection) with an id
        """
        directory_id = utils.str_to_swid(self.kwargs.get("Sha1"))
        return self._get_directory_by_id(directory_id)


class RevisionDirectoryNode(BaseDirectoryNode):
    def _get_node_data(self):
        """
        When a directory is requested from a revision
        """
        directory_id = self.kwargs.get("sha1")
        return self._get_directory_by_id(directory_id)
