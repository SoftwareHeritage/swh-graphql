from swh.graphql.backends import archive
from swh.graphql.utils import utils

from .base_node import BaseNode


class BaseDirectoryNode(BaseNode):
    def _get_directory_by_id(self, directory_id):
        # fetch more metadata like name
        return {
            "id": directory_id,
        }

    @property
    def entries(self):
        entries = archive.Archive().get_directory_entries(self._node.id)
        # FIXME, local pagination, should be moved to swh-storage (backend)
        # return Paginated(DirectoryEntryConnection, entries)
        return entries


class DirectoryNode(BaseDirectoryNode):
    def _get_node_data(self):
        """
        When a directory is requested directly
        (not from a connection) with an id
        """
        directory_id = utils.str_to_swid(self.kwargs.get("Sha1"))
        # path = ""
        return self._get_directory_by_id(directory_id)


class RevisionDirectoryNode(BaseDirectoryNode):
    def _get_node_data(self):
        """
        When a directory is requested from a revision
        """
        directory_id = self.kwargs.get("sha1")
        return self._get_directory_by_id(directory_id)
