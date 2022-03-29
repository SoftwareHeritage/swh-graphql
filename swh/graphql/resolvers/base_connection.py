"""
"""

from abc import ABC, abstractmethod

from swh.graphql.utils import utils

# from dataclasses import dataclass

# @dataclass
# class PageInfo:
#     nex_page_token: str


# class Arguments:
#     """
#     dataclass
#     """
#     after  # Elements that come after the specified cursor
#     first  # Returns the first n elements


class BaseConnection(ABC):
    _model_class = None

    def __init__(self, obj, info, **kwargs):
        self.obj = obj
        self.info = info
        self.kwargs = kwargs

        self._page_data = None

        self.pageInfo = self.page_info
        self.totalCount = self.total_count

    def __call__(self):
        return self

    @property
    def edges(self):
        return self._get_edges()

    @property
    def nodes(self):
        """
        Override if needed
        return a list of objects

        If a model class is set,
        return a list of its intance
        else a list of nodes
        """

        if self._model_class is not None:
            return [self._model_class(obj) for obj in self.page_data.results]
        return self.page_data.results

    @property
    def page_info(self):
        # FIXME Replace with a dataclass
        # return PageInfo(self.page_data.next_page_token)
        return {
            "hasNextPage": bool(self.page_data.next_page_token),
            "endCursor": utils.get_encoded_cursor(self.page_data.next_page_token),
        }

    @property
    def total_count(self):
        """
        Will be None for most of the connections
        override if needed
        """

        return None

    @property
    def page_data(self):
        """
        Cache to avoid multiple calls to
        the backend
        """

        if self._page_data is None:
            # FIXME, make this call async (not for v1)
            self._page_data = self._get_page_result()
        return self._page_data

    @abstractmethod
    def _get_page_result(self):
        """
        Override for desired behaviour
        return a PagedResult object
        """
        # FIXME, make this call async (not for v1)
        return None

    def _get_edges(self):
        return [{"cursor": "test", "node": each} for each in self.nodes]

    def _get_after_arg(self):
        """
        Return the decoded next page token
        override to use a specific token
        """
        return utils.get_decoded_cursor(self.kwargs.get("after"))

    def _get_first_arg(self):
        """
        Override to set the default page size
        """
        return self.kwargs.get("first", 50)
