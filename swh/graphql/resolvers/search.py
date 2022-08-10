# Copyright (C) 2022 The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information

from swh.graphql.backends import archive
from swh.storage.interface import PagedResult

from .base_connection import BaseConnection
from .base_node import BaseNode


class SearchResultNode(BaseNode):
    """ """


class ResolveSwhidConnection(BaseConnection):

    _node_class = SearchResultNode

    def _get_paged_result(self) -> PagedResult:
        swhid = self.kwargs.get("swhid")
        results = []
        if archive.Archive().is_object_available(swhid.object_id, swhid.object_type):
            results = [
                {
                    "target_hash": swhid.object_id,
                    "type": swhid.object_type.name.lower(),
                }
            ]
        return PagedResult(results=results)
