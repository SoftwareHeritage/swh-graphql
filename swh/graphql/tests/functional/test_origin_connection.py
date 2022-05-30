# Copyright (C) 2022 The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information

from ..data import get_origins
from .utils import get_query_response


def test_get(client, storage):
    query_str = """
    {
      origins(first: 10) {
        nodes {
          url
        }
      }
    }
    """
    data, _ = get_query_response(client, query_str)
    assert len(data["origins"]["nodes"]) == len(get_origins())


def test_get_filter_by_pattern(client):
    query_str = """
    {
      origins(first: 10, urlPattern: "somewhere.org/den") {
        nodes {
          url
        }
      }
    }
    """
    data, _ = get_query_response(client, query_str)
    assert len(data["origins"]["nodes"]) == 1


def test_get_filter_by_non_existing_pattern(client):
    query_str = """
    {
      origins(first: 10, urlPattern: "somewhere.org/den/test/") {
        nodes {
          url
        }
      }
    }
    """
    data, _ = get_query_response(client, query_str)
    assert len(data["origins"]["nodes"]) == 0


def test_basic_pagination(client):
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
