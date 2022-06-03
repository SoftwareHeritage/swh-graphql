# Copyright (C) 2022 The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Optional, Type

from swh.graphql.utils import utils

from .base_node import BaseNode


@dataclass
class PageInfo:
    hasNextPage: bool
    endCursor: str


@dataclass
class ConnectionEdge:
    node: Any
    cursor: str


class BaseConnection(ABC):
    """
    Base resolver for all the connections
    """

    _node_class: Optional[Type[BaseNode]] = None
    _page_size = 50  # default page size

    def __init__(self, obj, info, paged_data=None, **kwargs):
        self.obj = obj
        self.info = info
        self.kwargs = kwargs
        self._paged_data = paged_data

    def __call__(self, *args, **kw):
        return self

    @property
    def edges(self):
        return self._get_edges()

    @property
    def nodes(self):
        """
        Override if needed; return a list of objects

        If a node class is set, return a list of its (Node) instances
        else a list of raw results
        """
        if self._node_class is not None:
            return [
                self._node_class(self.obj, self.info, node_data=result, **self.kwargs)
                for result in self.get_paged_data().results
            ]
        return self.get_paged_data().results

    @property
    def pageInfo(self):  # To support the schema naming convention
        # FIXME, add more details like startCursor
        return PageInfo(
            hasNextPage=bool(self.get_paged_data().next_page_token),
            endCursor=utils.get_encoded_cursor(self.get_paged_data().next_page_token),
        )

    @property
    def totalCount(self):  # To support the schema naming convention
        return self._get_total_count()

    def _get_total_count(self):
        """
        Will be None for most of the connections
        override if needed/possible
        """
        return None

    def get_paged_data(self):
        """
        Cache to avoid multiple calls to
        the backend (_get_paged_result)
        return a PagedResult object
        """
        if self._paged_data is None:
            # FIXME, make this call async (not for v1)
            self._paged_data = self._get_paged_result()
        return self._paged_data

    @abstractmethod
    def _get_paged_result(self):
        """
        Override for desired behaviour
        return a PagedResult object
        """
        # FIXME, make this call async (not for v1)
        return None

    def _get_edges(self):
        """
        Return the list of connection edges, each with a cursor
        """
        return [
            ConnectionEdge(node=node, cursor=self._get_index_cursor(index, node))
            for (index, node) in enumerate(self.nodes)
        ]

    def _get_after_arg(self):
        """
        Return the decoded next page token
        override to use a specific token
        """
        return utils.get_decoded_cursor(self.kwargs.get("after"))

    def _get_first_arg(self):
        """
        page_size is set to 50 by default
        """
        return self.kwargs.get("first", self._page_size)

    def _get_index_cursor(self, index: int, node: Any):
        """
        Get the cursor to the given item index
        """
        # default implementation which works with swh-storage pagaination
        # override this function to support other types (eg: SnapshotBranchConnection)
        offset_index = self._get_after_arg() or "0"
        index_cursor = int(offset_index) + index
        return utils.get_encoded_cursor(str(index_cursor))
