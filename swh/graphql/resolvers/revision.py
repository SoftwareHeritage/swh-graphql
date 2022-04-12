from swh.graphql.backends import archive
from swh.graphql.utils import utils

from .base_node import BaseNode


class BaseRevisionNode(BaseNode):
    def _get_revision_by_id(self, revision_id):
        # FIXME, make this call async
        return (archive.Archive().get_revision(revision_id) or None)[0]

    @property
    def author(self):
        # return a PersoneNode object
        return self._node.author

    @property
    def committer(self):
        # return a PersoneNode object
        return self._node.committer

    @property
    def parentIds(self):  # To support the schema naming convention
        return self._node.parents

    @property
    def parents(self):
        """
        Return a list of parent revisions
        """
        # FIXME, change this to a paginated list
        # Storage fix or use local paginator
        # Move to resolvers.resolvers.py

        return [
            ParentRevisionNode(obj=self, info=self.info, sha1=revision_id)
            for revision_id in self.parentIds
        ]

    @property
    def directoryId(self):  # To support the schema naming convention
        """ """
        return self._node.directory

    def is_type_of(self):
        """
        is_type_of is required only when
        requesting from a connection

        This is for ariadne to return the correct type in schema
        """
        return "Revision"


class RevisionNode(BaseRevisionNode):
    """
    When the revision is requested directly
    (not from a connection) with an id
    """

    def _get_node_data(self):
        revision_id = utils.str_to_swid(self.kwargs.get("Sha1"))
        return self._get_revision_by_id(revision_id)


class ParentRevisionNode(BaseRevisionNode):
    """
    When a parent revision is requested
    from a revision
    """

    # This class will be removed onece ParentRevisionConnection
    # is implemented
    def _get_node_data(self):
        revision_id = self.kwargs.get("sha1")
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
        return self._get_revision_by_id(self.obj.target)
