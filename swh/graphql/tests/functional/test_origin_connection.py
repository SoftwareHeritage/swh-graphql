# Copyright (C) 2022 The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information

from .utils import get_query_response


def test_get(client):
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
    assert len(data["origins"]["nodes"]) == 2


def test_get_filter_by_pattern(client):
    query_str = """
    {
      origins(first: 10, urlPattern: "forge1") {
        nodes {
          url
        }
      }
    }
    """
    data, _ = get_query_response(client, query_str)
    assert len(data["origins"]["nodes"]) == 1


def test_basic_pagination(client):
    query_str = """
    {
      origins(first: 2) {
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
    assert len(data["origins"]["nodes"]) == 2
    assert data["origins"]["pageInfo"] == {"hasNextPage": False, "endCursor": None}
