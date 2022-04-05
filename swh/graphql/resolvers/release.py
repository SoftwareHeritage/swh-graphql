from swh.graphql.backends import archive

from .base_node import BaseNode


class ReleaseNode(BaseNode):
    def _get_node_data(self):
        """
        """


class BranchReleaseNode(BaseNode):
    """
    When the release is requested from
    a snapshot branch
    self.obj is a branch object
    self.obj.target is the release id
    """

    def _get_node_data(self):
        k = (archive.Archive().get_release(self.obj.target) or None)[0]
        return k

    def is_type_of(self):
        """
        is_type_of is required only when
        requesting from a connection

        This is for ariadne to return the correct type in schema
        """
        return "Release"

    @property
    def author(self):
        # return a PersoneNode object
        return self.obj.author
