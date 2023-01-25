# Copyright (C) 2022 The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information

from __future__ import annotations

from .base_connection import BaseConnection, BaseList, ConnectionData
from .base_node import BaseNode


class SearchResultNode(BaseNode):
    """ """

    @property
    def targetType(self):  # To support the schema naming convention
        return self._node.type


class ResolveSwhidList(BaseList):

    _node_class = SearchResultNode

    def _get_results(self) -> list:
        swhid = self.kwargs.get("swhid")
        results = []

        if self.archive.is_object_available(swhid.object_id, swhid.object_type):
            results = [
                {
                    "target_hash": swhid.object_id,
                    "type": swhid.object_type.name.lower(),
                }
            ]
        return results


class OriginSearchResultNode(BaseNode):

    obj: OriginSearchConnection

    def _get_node_from_data(self, node_data: dict):
        # overriding to enrich the node_data returned
        # by OriginSearchConnection._get_connection_data
        updated_node_data = {
            # Field exposed in the schema
            "type": "origin",
            # Field exposed in the schema
            "url": node_data.get("url"),
            # Field NOT exposed in the schema, used to get the target node
            "target_url": node_data.get("url"),
        }
        return super()._get_node_from_data(updated_node_data)


class OriginSearchConnection(BaseConnection):

    _node_class = OriginSearchResultNode

    def _get_connection_data(self) -> ConnectionData:
        origins = self.search.get_origins(
            query=self.kwargs.get("query"),
            after=self._get_after_arg(),
            first=self._get_first_arg(),
        )
        return ConnectionData(paged_result=origins)
