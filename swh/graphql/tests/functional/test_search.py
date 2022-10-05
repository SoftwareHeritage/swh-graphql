# Copyright (C) 2022 The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information

from . import utils


def test_search_origins(client):
    query_str = """
    query doSearch($query: String!, $first: Int!) {
      search(query: $query, first: $first) {
        nodes {
          targetType
          target {
            ...on Origin {
              url
              latestVisit {
                date
              }
            }
          }
        }
        pageInfo {
          hasNextPage
          endCursor
        }
      }
    }
    """
    data, _ = utils.get_query_response(client, query_str, query="fox", first=1)
    assert len(data["search"]["nodes"]) == 1
    assert data == {
        "search": {
            "nodes": [
                {
                    "target": {
                        "url": "https://somewhere.org/den/fox",
                        "latestVisit": {"date": "2018-11-27T17:20:39+00:00"},
                    },
                    "targetType": "origin",
                }
            ],
            "pageInfo": {"endCursor": "MQ==", "hasNextPage": True},
        }
    }


def test_search_missing_url(client):
    query_str = """
    query doSearch($query: String!, $first: Int!) {
      search(query: $query, first: $first) {
        nodes {
          targetType
        }
        pageInfo {
          hasNextPage
          endCursor
        }
      }
    }
    """
    data, _ = utils.get_query_response(client, query_str, query="missing-fox", first=1)
    assert len(data["search"]["nodes"]) == 0
