# Copyright (C) 2022 The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information

from .utils import get_query_response


def test_invalid_get(client):
    query_str = """
    {
      origin(url: "http://example.com/forge1/") {
        url
      }
    }
    """
    data, errors = get_query_response(client, query_str)
    assert data["origin"] is None
    assert len(errors) == 1
    assert errors[0]["message"] == "Requested object is not available"


def test_get(client):
    query_str = """
    {
      origin(url: "http://example.com/forge1") {
        url
        id
        visits(first: 10) {
          nodes {
            id
          }
        }
        latestVisit {
          visitId
        }
        snapshots(first: 2) {
          nodes {
            id
          }
        }
      }
    }
    """
    data, _ = get_query_response(client, query_str)
    origin = data["origin"]
    assert origin["url"] == "http://example.com/forge1"
    assert len(origin["visits"]["nodes"]) == 2
    assert origin["latestVisit"]["visitId"] == 2
    assert len(origin["snapshots"]["nodes"]) == 1
