from swh.graphql.utils import utils

from .base_node import BaseNode


class BaseDirectoryNode(BaseNode):
    def _get_directory_by_id(self, directory_id):
        # Now not fetching any data (schema is exposing just id)
        # same pattern is used in snapshot resolver
        # FIXME, use the right API to fetch metadata like name, path
        return {
            "id": directory_id,
        }

    def is_type_of(self):
        return "Directory"


class DirectoryNode(BaseDirectoryNode):
    def _get_node_data(self):
        """
        When a directory is requested directly with an id
        """
        directory_id = utils.str_to_sha1(self.kwargs.get("Sha1"))
        # path = ""
        return self._get_directory_by_id(directory_id)


class RevisionDirectoryNode(BaseDirectoryNode):
    def _get_node_data(self):
        """
        When a directory is requested from a revision
        self.obj is revision here
        self.obj.directoryId is the required dir id
        (set from resolvers.revision.py:BaseRevisionNode)
        """
        directory_id = self.obj.directoryId
        return self._get_directory_by_id(directory_id)


class TargetDirectoryNode(BaseDirectoryNode):
    def _get_node_data(self):
        """
        When a directory is requested as a target
        self.obj can be a Release or a DirectoryEntry

        obj.target is the requested directory id here
        """
        return self._get_directory_by_id(self.obj.target)
