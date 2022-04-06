from swh.graphql.backends import archive
from swh.graphql.utils import utils

from .base_node import BaseNode


class BaseRevisionNode(BaseNode):
    def _get_revision_by_id(self, revision_id):
        return (archive.Archive().get_revision(revision_id) or None)[0]

    @property
    def author(self):
        # return a PersoneNode object
        return self._node.author

    @property
    def committer(self):
        # return a PersoneNode object
        return self._node.committer


class RevisionNode(BaseRevisionNode):
    """
    When the revision is requested directly
    (not from a connection) with an id
    """

    def _get_node_data(self):
        revision_id = utils.str_to_swid(self.kwargs.get("SWHId"))
        return self._get_revision_by_id(revision_id)


class BranchRevisionNode(BaseRevisionNode):
    """
    When the revision is requested from
    a snapshot branch
    self.obj is a branch object
    self.obj.target is the revision id
    """

    def _get_node_data(self):
        """
        self.obj.target is the Revision id
        """
        # FIXME, make this call async (not for v1)
        return self._get_revision_by_id(self.obj.target)

    def is_type_of(self):
        """
        is_type_of is required only when
        requesting from a connection

        This is for ariadne to return the correct type in schema
        """
        return "Revision"
