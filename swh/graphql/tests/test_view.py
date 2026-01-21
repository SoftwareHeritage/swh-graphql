# Copyright (C) 2023  The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information


def test_view(client):
    response = client.get("/")
    assert "<title>SWH GraphQL explorer</title>" in response.text
    assert "login</a>" in response.text
    assert "<span>Software Heritage GraphQL Explorer</span>" in response.text
