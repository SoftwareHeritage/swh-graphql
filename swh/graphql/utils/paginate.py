"""
Pagination at the GraphQL level
This is a temporary fix and inefficient.
Should eventually be moved to the
backend (storage) level
"""


class PaginatedList:
    def __init__(self, source):
        """
        source can be of any iterable type
        """
        self.source = source

    def get_items(self, first, after):
        """
        Return the 'first' number of
        items 'after' the given cursor
        """
        return self.source[after : (after + first)]

    def get_item_objects(self, first, after):
        """
        Return the 'first' number of
        items 'after' the given cursor
        with an item cursor
        """
        return [
            {"curosr": first + index, "node": item}
            for (index, item) in enumerate(self.get_items(first, after), 1)
        ]
