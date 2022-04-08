from swh.graphql.backends import archive
from swh.graphql.utils import utils

from .base_node import BaseNode


class BaseReleaseNode(BaseNode):
    def _get_release_by_id(self, release_id):
        return (archive.Archive().get_release(release_id) or None)[0]

    @property
    def author(self):
        # return a PersoneNode object
        return self._node.author

    def is_type_of(self):
        """
        is_type_of is required only when requesting
        from a connection

        This is for ariadne to return the right type
        """
        return "Release"


class ReleaseNode(BaseReleaseNode):
    """
    When the release is requested directly
    (not from a connection) with an id
    """

    def _get_node_data(self):
        release_id = utils.str_to_swid(self.kwargs.get("Sha1"))
        return self._get_release_by_id(release_id)


class BranchReleaseNode(BaseReleaseNode):
    """
    When the release is requested from
    a snapshot branch
    self.obj is a branch object
    self.obj.target is the release id
    """

    def _get_node_data(self):
        return self._get_release_by_id(self.obj.target)
