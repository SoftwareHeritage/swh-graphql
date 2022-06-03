# Copyright (C) 2022 The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information

from ..data import get_origins
from .utils import get_query_response


# Using Origin object to run functional tests for pagination
def test_pagination(client):
    # requesting the max number of nodes available
    # endCursor must be None
    query_str = f"""
    {{
      origins(first: {len(get_origins())}) {{
        nodes {{
          id
        }}
        pageInfo {{
          hasNextPage
          endCursor
        }}
      }}
    }}
    """

    data, _ = get_query_response(client, query_str)
    assert len(data["origins"]["nodes"]) == len(get_origins())
    assert data["origins"]["pageInfo"] == {"hasNextPage": False, "endCursor": None}


def get_first_node(client):
    query_str = """
    {
      origins(first: 1) {
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
    data, _ = get_query_response(client, query_str)
    return data["origins"]


def test_first_arg(client):
    origins = get_first_node(client)
    assert len(origins["nodes"]) == 1
    assert origins["pageInfo"]["hasNextPage"] is True


def test_after_arg(client):
    origins = get_first_node(client)
    end_cursor = origins["pageInfo"]["endCursor"]
    query_str = f"""
    {{
      origins(first: 1, after: "{end_cursor}") {{
        nodes {{
          id
        }}
        pageInfo {{
          hasNextPage
          endCursor
        }}
      }}
    }}
    """
    data, _ = get_query_response(client, query_str)
    assert len(data["origins"]["nodes"]) == 1
    assert data["origins"]["pageInfo"] == {"hasNextPage": False, "endCursor": None}


def test_edge_cursor(client):
    origins = get_first_node(client)
    # end cursor here must be the item cursor for the second item
    end_cursor = origins["pageInfo"]["endCursor"]

    query_str = f"""
    {{
      origins(first: 1, after: "{end_cursor}") {{
        edges {{
          cursor
          node {{
            id
          }}
        }}
        nodes {{
          id
        }}
      }}
    }}
    """
    data, _ = get_query_response(client, query_str)
    origins = data["origins"]
    assert [edge["node"] for edge in origins["edges"]] == origins["nodes"]
    assert origins["edges"][0]["cursor"] == end_cursor
