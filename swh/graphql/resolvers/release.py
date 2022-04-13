from swh.graphql.backends import archive
from swh.graphql.utils import utils

from .base_node import BaseNode


class BaseReleaseNode(BaseNode):
    def _get_release_by_id(self, release_id):
        return (archive.Archive().get_releases([release_id]) or None)[0]

    @property
    def targetId(self):  # To support the schema naming convention
        return self._node.target

    @property
    def type(self):
        return self._node.target_type.value

    def is_type_of(self):
        """
        is_type_of is required only when resolving
        a UNION type
        This is for ariadne to return the right type
        """
        return "Release"


class ReleaseNode(BaseReleaseNode):
    """
    When the release is requested directly with an id
    """

    def _get_node_data(self):
        release_id = utils.str_to_swid(self.kwargs.get("Sha1"))
        return self._get_release_by_id(release_id)


class TargetReleaseNode(BaseReleaseNode):
    """
    When a release is requested as a target

    self.obj could be a snapshotbranch or a release
    self.obj.target is the requested release id here
    """

    def _get_node_data(self):
        return self._get_release_by_id(self.obj.target)
