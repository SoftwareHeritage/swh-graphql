# Copyright (C) 2022 The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information

import base64
from datetime import datetime
from typing import List

from swh.storage.interface import PagedResult

ENCODING = "utf-8"


def get_b64_string(source) -> str:
    if type(source) is str:
        source = source.encode(ENCODING)
    return base64.b64encode(source).decode("ascii")


def get_encoded_cursor(cursor: str) -> str:
    if cursor is None:
        return None
    return get_b64_string(cursor)


def get_decoded_cursor(cursor: str) -> str:
    if cursor is None:
        return None
    return base64.b64decode(cursor).decode(ENCODING)


def str_to_sha1(sha1: str) -> bytearray:
    # FIXME, use core function
    return bytearray.fromhex(sha1)


def get_formatted_date(date: datetime) -> str:
    # FIXME, handle error + return other formats
    return date.isoformat()


def paginated(source: List, first: int, after=0) -> PagedResult:
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
