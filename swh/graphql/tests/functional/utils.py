# Copyright (C) 2022 The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information

import json


def get_query_response(client, query_str):
    response = client.post("/", json={"query": query_str})
    assert response.status_code == 200, response.data
    result = json.loads(response.data)
    return result.get("data"), result.get("errors")
