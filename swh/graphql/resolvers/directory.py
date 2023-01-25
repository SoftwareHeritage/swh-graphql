# Copyright (C) 2022 The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information

from typing import TYPE_CHECKING, Union

from swh.model.model import Directory
from swh.model.swhids import ObjectType

from .base_node import BaseSWHNode
from .search import SearchResultNode


class BaseDirectoryNode(BaseSWHNode):
    """
    Base resolver for all the directory nodes
    """

    def _get_directory_by_id(self, directory_id):
        # Return a Directory model object
        # entries is initialized as empty
        # Same pattern is used in snapshot
        return Directory(id=directory_id, entries=())

    def is_type_of(self):
        return "Directory"


class DirectoryNode(BaseDirectoryNode):
    """
    Node resolver for a directory requested directly with its SWHID
    """

    def _get_node_data(self):
        swhid = self.kwargs.get("swhid")
        if (
            swhid.object_type == ObjectType.DIRECTORY
            and self.archive.is_object_available(swhid.object_id, swhid.object_type)
        ):
            # _get_directory_by_id is not making any backend call
            # hence the is_directory_available validation
            return self._get_directory_by_id(swhid.object_id)
        return None


class TargetDirectoryNode(BaseDirectoryNode):
    """
    Node resolver for a directory requested as a target
    """

    if TYPE_CHECKING:  # pragma: no cover
        from .target import BranchTargetNode, TargetNode

        obj: Union[
            BranchTargetNode,
            TargetNode,
            SearchResultNode,
        ]
    _can_be_null = True

    def _get_node_data(self):
        if self.obj.target_hash:
            return self._get_directory_by_id(self.obj.target_hash)
        return None
