"""
"""
# from dataclasses import dataclass


# class PageInfo:
#     """
#     dataclass
#     """

# class Arguments:
#     """
#     dataclass
#     """
#     after  # Elements that come after the specified cursor
#     first  # Returns the first n elements


class BaseConnection:
    @property
    def edges(self):
        pass

    @property
    def nodes(self):
        pass

    @property
    def page_info(self):
        return {
            "hasNextPage": True,
            "endCursor": "",
        }

    @property
    def total_count(self):
        return 0
