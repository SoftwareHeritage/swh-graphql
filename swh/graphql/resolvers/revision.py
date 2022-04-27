from swh.graphql.backends import archive
from swh.graphql.utils import utils

from .base_connection import BaseConnection
from .base_node import BaseNode


class BaseRevisionNode(BaseNode):
    def _get_revision_by_id(self, revision_id):
        return (archive.Archive().get_revisions([revision_id]) or None)[0]

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
        is_type_of is required only when resolving
        a UNION type
        This is for ariadne to return the right type
        """
        return "Revision"


class RevisionNode(BaseRevisionNode):
    """
    When the revision is requested directly with its id (hash)
    """

    def _get_node_data(self):
        return self._get_revision_by_id(self.kwargs.get("SWHID").object_id)


class TargetRevisionNode(BaseRevisionNode):
    """
    When a revision is requested as a target

    self.obj could be a snapshotbranch or a release
    self.obj.target is the requested revision id here
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
    self.obj is the current(child) revision
    self.obj.parentIds is the list of
    requested revisions
    """

    _node_class = BaseRevisionNode

    def _get_paged_result(self):
        # FIXME, using dummy(local) pagination, move pagination to backend
        # To remove localpagination, just drop the paginated call
        # STORAGE-TODO (pagination)
        parents = archive.Archive().get_revisions(self.obj.parentIds)
        return utils.paginated(parents, self._get_first_arg(), self._get_after_arg())


class LogRevisionConnection(BaseConnection):
    """
    When revisionslog is requested from a
    revision
    self.obj is the current revision id
    """

    _node_class = BaseRevisionNode

    def _get_paged_result(self):
        # STORAGE-TODO (date in revisionlog is a dict)
        log = archive.Archive().get_revision_log([self.obj.id])
        # FIXME, using dummy(local) pagination, move pagination to backend
        # To remove localpagination, just drop the paginated call
        # STORAGE-TODO (pagination)
        return utils.paginated(log, self._get_first_arg(), self._get_after_arg())
