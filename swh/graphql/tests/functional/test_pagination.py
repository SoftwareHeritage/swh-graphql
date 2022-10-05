# Copyright (C) 2022 The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information

from . import utils
from ..data import get_origins


# Using Origin object to run functional tests for pagination
def get_origin_nodes(client, first, after=""):
    query_str = """
    query getOrigins($first: Int!, $after: String) {
      origins(first: $first, after: $after) {
        nodes {
          id
        }
        pageInfo {
          hasNextPage
          endCursor
        }
      }
    }
    """
    return utils.get_query_response(client, query_str, first=first, after=after)


def test_pagination(client):
    # requesting the max number of nodes available
    # endCursor must be None
    data, _ = get_origin_nodes(client, first=len(get_origins()))
    assert len(data["origins"]["nodes"]) == len(get_origins())
    assert data["origins"]["pageInfo"] == {"hasNextPage": False, "endCursor": None}


def test_first_arg(client):
    data, _ = get_origin_nodes(client, first=1)
    assert len(data["origins"]["nodes"]) == 1
    assert data["origins"]["pageInfo"]["hasNextPage"] is True


def test_invalid_first_arg(client):
    data, errors = get_origin_nodes(client, first=-1)
    assert data["origins"] is None
    assert (len(errors)) == 2  # one error for origins and anotehr one for pageInfo
    assert (
        errors[0]["message"]
        == "Pagination error: Value for argument 'first' is invalid; it must be between 0 and 1000"  # noqa: B950
    )


def test_too_big_first_arg(client):
    data, errors = get_origin_nodes(client, first=1001)  # max page size is 1000
    assert data["origins"] is None
    assert (len(errors)) == 2
    assert (
        errors[0]["message"]
        == "Pagination error: Value for argument 'first' is invalid; it must be between 0 and 1000"  # noqa: B950
    )


def test_after_arg(client):
    first_data, _ = get_origin_nodes(client, first=1)
    end_cursor = first_data["origins"]["pageInfo"]["endCursor"]
    # get again with endcursor as the after argument
    data, _ = get_origin_nodes(client, first=1, after=end_cursor)
    assert len(data["origins"]["nodes"]) == 1
    assert data["origins"]["pageInfo"] == {"hasNextPage": False, "endCursor": None}


def test_invalid_after_arg(client):
    data, errors = get_origin_nodes(client, first=1, after="invalid")
    assert data["origins"] is None
    assert (len(errors)) == 2
    assert (
        errors[0]["message"] == "Pagination error: Invalid value for argument 'after'"
    )


def test_edge_cursor(client):
    origins = get_origin_nodes(client, first=1)[0]["origins"]
    # end cursor here must be the item cursor for the second item
    end_cursor = origins["pageInfo"]["endCursor"]

    query_str = """
    query getOrigins($first: Int!, $after: String) {
      origins(first: $first, after: $after) {
        edges {
          cursor
          node {
            id
          }
        }
        nodes {
          id
        }
      }
    }
    """
    data, _ = utils.get_query_response(client, query_str, first=1, after=end_cursor)
    origins = data["origins"]
    assert [edge["node"] for edge in origins["edges"]] == origins["nodes"]
    assert origins["edges"][0]["cursor"] == end_cursor
