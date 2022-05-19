# Copyright (C) 2022 The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information

from swh.graphql.backends import archive
from swh.graphql.utils import utils

from .base_connection import BaseConnection
from .base_node import BaseNode


class DirectoryEntryNode(BaseNode):
    """ """

    @property
    def targetHash(self):  # To support the schema naming convention
        return self._node.target


class DirectoryEntryConnection(BaseConnection):
    _node_class = DirectoryEntryNode

    def _get_paged_result(self):
        """
        When entries requested from a directory
        self.obj.swhid is the directory SWHID here

        This is not paginated from swh-storgae
        using dummy pagination
        """

        # FIXME, using dummy(local) pagination, move pagination to backend
        # To remove localpagination, just drop the paginated call
        # STORAGE-TODO
        entries = (
            archive.Archive().get_directory_entries(self.obj.swhid.object_id).results
        )
        return utils.paginated(entries, self._get_first_arg(), self._get_after_arg())
