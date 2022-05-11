# Copyright (C) 2022 The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information

from swh.graphql.backends import archive

from .base_connection import BaseConnection
from .base_node import BaseSWHNode


class OriginNode(BaseSWHNode):
    def _get_node_data(self):
        return archive.Archive().get_origin(self.kwargs.get("url"))


class OriginConnection(BaseConnection):
    _node_class = OriginNode

    def _get_paged_result(self):
        return archive.Archive().get_origins(
            after=self._get_after_arg(),
            first=self._get_first_arg(),
            url_pattern=self.kwargs.get("urlPattern"),
        )
