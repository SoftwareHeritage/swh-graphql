# Copyright (C) 2022 The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information

import pytest

from ..data import get_visit_status, get_visits
from .utils import get_query_response


@pytest.mark.parametrize(
    "visit, visit_status", list(zip(get_visits(), get_visit_status()))
)
def test_get_visit_status(client, visit, visit_status):
    query_str = """
    {
      visit(originUrl: "%s", visitId: %s) {
        status(first: 3) {
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
    assert data["visit"]["status"]["nodes"][0] == {
        "date": visit_status.date.isoformat(),
        "snapshot": {"swhid": f"swh:1:snp:{visit_status.snapshot.hex()}"}
        if visit_status.snapshot is not None
        else None,
        "status": visit_status.status,
        "type": visit_status.type,
    }
