import base64

from swh.storage.interface import PagedResult


def encode(text):
    return base64.b64encode(bytes(text, "utf-8")).decode("utf-8")


def get_encoded_cursor(cursor):
    if cursor is None:
        return None
    return base64.b64encode(bytes(cursor, "utf-8")).decode("utf-8")


def get_decoded_cursor(cursor):
    if cursor is None:
        return None
    return base64.b64decode(cursor).decode("utf-8")


def str_to_swid(str_swid):
    # FIXME, use core function
    return bytearray.fromhex(str_swid)


def paginated(source, first, after=0):
    """
    Pagination at the GraphQL level
    This is a temporary fix and inefficient.
    Should eventually be moved to the
    backend (storage) level
    """

    # FIXME, handle data errors here
    after = 0 if after is None else int(after)
    end_cursor = after + first
    results = source[after:end_cursor]
    next_page_token = None
    if len(source) > end_cursor:
        next_page_token = str(end_cursor)
    return PagedResult(results=results, next_page_token=next_page_token)
