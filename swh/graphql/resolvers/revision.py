from swh.graphql.backends import archive

from .base_node import BaseNode


class RevisionNode(BaseNode):
    """
    When the revision is requested
    directly using an id
    """

    def _get_node_data(self):
        """
        """


class BranchRevisionNode(BaseNode):
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
        # k = (archive.Archive().get_revision(self.obj.target) or None)[0]
        # import pdb; pdb.set_trace()
        return (archive.Archive().get_revision(self.obj.target) or None)[0]

    def is_type_of(self):
        """
        is_type_of is required only when
        requesting from a connection

        This is for ariadne to return the correct type in schema
        """
        # FIXME, this is coupled with the schema
        return "Revision"
