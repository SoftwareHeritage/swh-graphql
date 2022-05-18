# Copyright (C) 2022 The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information

from swh.graphql.backends import archive

from .base_node import BaseSWHNode


class BaseContentNode(BaseSWHNode):
    """ """

    def _get_content_by_id(self, content_id):
        content = archive.Archive().get_content(content_id)
        return content[0] if content else None

    @property
    def checksum(self):
        # FIXME, return a Node object
        return {k: v.hex() for (k, v) in self._node.hashes().items()}

    @property
    def id(self):
        return self._node.sha1_git

    def is_type_of(self):
        return "Content"


class ContentNode(BaseContentNode):
    def _get_node_data(self):
        """
        When a content is requested directly
        with its SWHID
        """
        return self._get_content_by_id(self.kwargs.get("SWHID").object_id)


class TargetContentNode(BaseContentNode):
    def _get_node_data(self):
        """
        When a content is requested from a
        directory entry or from a release target

        content id is obj.targetHash here
        """
        content_id = self.obj.targetHash
        return self._get_content_by_id(content_id)
