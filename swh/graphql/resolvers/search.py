# Copyright (C) 2022 The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information

from swh.storage.interface import PagedResult

from .base_connection import BaseConnection
from .base_node import BaseNode


class SearchResultNode(BaseNode):
    """ """

    @property
    def targetType(self):  # To support the schema naming convention
        return self._node.type


class ResolveSwhidConnection(BaseConnection):

    _node_class = SearchResultNode

    def _get_paged_result(self) -> PagedResult:
        swhid = self.kwargs.get("swhid")
        results = []
        if self.archive.is_object_available(swhid.object_id, swhid.object_type):
            results = [
                {
                    "target_hash": swhid.object_id,
                    "type": swhid.object_type.name.lower(),
                }
            ]
        return PagedResult(results=results)


class SearchConnection(BaseConnection):

    _node_class = SearchResultNode

    def _get_paged_result(self) -> PagedResult:
        origins = self.search.get_origins(
            query=self.kwargs.get("query"),
            after=self._get_after_arg(),
            first=self._get_first_arg(),
        )

        # FIXME hard coding type to origin for now, as it is the only searchable object
        results = [
            {"target_url": ori["url"], "type": "origin"} for ori in origins.results
        ]
        return PagedResult(results=results, next_page_token=origins.next_page_token)
