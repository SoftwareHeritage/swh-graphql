"""
"""
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


class BaseConnection:
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
        return self.page_data.results

    @property
    def page_info(self):
        # return PageInfo(self.page_data.next_page_token)
        return {
            "hasNextPage": bool(self.page_data.next_page_token),
            "endCursor": self.page_data.next_page_token,
        }

    @property
    def total_count(self):
        """
        Will be None for most of the connections
        """

        return None

    @property
    def page_data(self):
        """
        Cache to avoid multiple calls to
        the backend
        """

        if self._page_data is None:
            # FIXME, make this call async
            self._page_data = self._get_page_results()
        return self._page_data

    def _get_page_results(self):
        """
        Override for desired behaviour
        """

        return None

    def _get_edges(self):
        return [{"cursor": "test", "node": each} for each in self.page_data.results]

    def _encode_cursor(self):
        # FIXME, move to utils
        pass

    def _decode_cursor(self):
        # FIXME, move to utils
        pass
