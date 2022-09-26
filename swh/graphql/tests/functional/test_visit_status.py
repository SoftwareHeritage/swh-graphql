# Copyright (C) 2022 The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information

import pytest

from ..data import get_origins, get_visit_status, get_visits
from .utils import get_query_response


@pytest.mark.parametrize(
    "visit, visit_status", list(zip(get_visits(), get_visit_status()))
)
def test_get_visit_status(client, visit, visit_status):
    query_str = """
    {
      visit(originUrl: "%s", visitId: %s) {
        statuses(first: 3) {
          nodes {
            status
            date
            type
            snapshot {
              swhid
            }
          }
        }
      }
    }
    """ % (
        visit.origin,
        visit.visit,
    )
    data, _ = get_query_response(client, query_str)
    assert data["visit"]["statuses"]["nodes"][0] == {
        "date": visit_status.date.isoformat(),
        "snapshot": {"swhid": f"swh:1:snp:{visit_status.snapshot.hex()}"}
        if visit_status.snapshot is not None
        else None,
        "status": visit_status.status,
        "type": visit_status.type,
    }


def test_visit_status_pagination(client):
    # visit status is using a different cursor, hence separate test
    query_str = """
    {
      visit(originUrl: "%s", visitId: %s) {
        statuses(first: 1) {
          pageInfo {
            hasNextPage
            endCursor
          }
          edges {
            cursor
            node {
              status
            }
          }
        }
      }
    }
    """ % (
        get_origins()[0].url,
        1,
    )
    data, _ = get_query_response(client, query_str)
    # request again with the endcursor
    end_cursor = data["visit"]["statuses"]["pageInfo"]["endCursor"]
    query_str = """
    {
      visit(originUrl: "%s", visitId: %s) {
        statuses(first: 1, after: "%s") {
          pageInfo {
            hasNextPage
            endCursor
          }
          edges {
            cursor
            node {
              status
            }
          }
        }
      }
    }
    """ % (
        get_origins()[0].url,
        1,
        end_cursor,
    )
    data, _ = get_query_response(client, query_str)
    assert data["visit"]["statuses"] == {
        "edges": [
            {
                "cursor": "MjAxNC0wNS0wN1QwNDoyMDozOS40MzIyMjIrMDA6MDA=",
                "node": {"status": "ongoing"},
            }
        ],
        "pageInfo": {"endCursor": None, "hasNextPage": False},
    }
