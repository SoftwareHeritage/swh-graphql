from swh.graphql.backends import archive
from swh.graphql.utils import utils

from .base_connection import BaseConnection
from .base_node import BaseNode


class BaseRevisionNode(BaseNode):
    def _get_revision_by_id(self, revision_id):
        # FIXME, make this call async
        return (archive.Archive().get_revisions([revision_id]) or None)[0]

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
    def directoryId(self):  # To support the schema naming convention
        """ """
        return self._node.directory

    @property
    def type(self):
        return self._node.type.value

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


class TargetRevisionNode(BaseRevisionNode):
    """
    When a revision is requested as a target

    self.obj could be a snapshotbranch or a release
    self.obj.target is the revision id here
    """

    def _get_node_data(self):
        """
        self.obj.target is the Revision id
        """
        return self._get_revision_by_id(self.obj.target)


class ParentRevisionConnection(BaseConnection):
    """
    When parent revisions requested from a
    revision
    self.obj is the child revision here
    self.obj.parentIds is the list of
    parent revisions
    """

    _node_class = BaseRevisionNode

    def _get_paged_result(self):
        # FIXME, using dummy(local) pagination, move pagination to backend
        # To remove localpagination, just drop the paginated call
        parents = archive.Archive().get_revisions(self.obj.parentIds)
        return utils.paginated(parents, self._get_first_arg(), self._get_after_arg())
