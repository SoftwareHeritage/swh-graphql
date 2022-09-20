# Copyright (C) 2022 The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information

from swh.graphql.utils import utils
from swh.storage.interface import PagedResult

from .base_connection import BaseConnection
from .base_node import BaseNode


class BaseDirectoryEntryNode(BaseNode):
    @property
    def target_hash(self):  # for DirectoryNode
        return self._node.target

    @property
    def targetType(self):  # To support the schema naming convention
        mapping = {"file": "content", "dir": "directory", "rev": "revision"}
        return mapping.get(self._node.type)


class DirectoryEntryNode(BaseDirectoryEntryNode):
    """
    Node resolver for a directory entry requested with a
    directory SWHID and a relative path
    """

    def _get_node_data(self):
        # STORAGE-TODO, archive is returning a dict
        # return DirectoryEntry object instead
        return self.archive.get_directory_entry_by_path(
            directory_id=self.kwargs.get("directorySwhid").object_id,
            path=self.kwargs.get("path"),
        )


class DirectoryEntryConnection(BaseConnection):
    """
    Connection resolver for entries in a directory
    """

    from .directory import BaseDirectoryNode

    obj: BaseDirectoryNode

    _node_class = BaseDirectoryEntryNode

    def _get_paged_result(self) -> PagedResult:
        # FIXME, using dummy(local) pagination, move pagination to backend
        # To remove localpagination, just drop the paginated call
        # STORAGE-TODO
        entries = self.archive.get_directory_entries(self.obj.swhid.object_id).results
        name_include = self.kwargs.get("nameInclude")
        if name_include is not None:
            # STORAGE-TODO, move this filter to swh-storage
            entries = [
                x for x in entries if name_include.lower().encode() in x.name.lower()
            ]
        return utils.paginated(entries, self._get_first_arg(), self._get_after_arg())
