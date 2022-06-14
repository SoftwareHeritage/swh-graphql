# Copyright (C) 2022 The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information

import pytest

from .utils import get_query_response


def test_get(client):
    query_str = """
    {
      snapshot(swhid: "swh:1:snp:0e7f84ede9a254f2cd55649ad5240783f557e65f") {
        branches(first:10) {
          nodes {
            type
            target {
              __typename
              ...on Revision {
                swhid
              }
              ...on Release {
                swhid
              }
              ...on Content {
                swhid
              }
              ...on Directory {
                swhid
              }
              ...on Snapshot {
                swhid
              }
            }
          }
        }
      }
    }
    """
    data, errors = get_query_response(client, query_str)
    # Alias type is not handled at the moment, hence the error
    assert len(errors) == 1
    assert errors[0]["message"] == "Invalid node type: branch-alias"
    assert len(data["snapshot"]["branches"]["nodes"]) == 5


@pytest.mark.parametrize(
    "filter_type, count, target_type, swhid_pattern",
    [
        ("revision", 1, "Revision", "swh:1:rev"),
        ("release", 1, "Release", "swh:1:rel"),
        ("directory", 1, "Directory", "swh:1:dir"),
        ("content", 0, "Content", "swh:1:cnt"),
        ("snapshot", 1, "Snapshot", "swh:1:snp"),
    ],
)
def test_get_type_filter(client, filter_type, count, target_type, swhid_pattern):
    query_str = (
        """
    {
      snapshot(swhid: "swh:1:snp:0e7f84ede9a254f2cd55649ad5240783f557e65f") {
        branches(first:10, types: [%s]) {
          nodes {
            type
            target {
              __typename
              ...on Revision {
                swhid
              }
              ...on Release {
                swhid
              }
              ...on Content {
                swhid
              }
              ...on Directory {
                swhid
              }
              ...on Snapshot {
                swhid
              }
            }
          }
        }
      }
    }
    """
        % filter_type
    )
    data, _ = get_query_response(client, query_str)

    assert len(data["snapshot"]["branches"]["nodes"]) == count
    for node in data["snapshot"]["branches"]["nodes"]:
        assert node["target"]["__typename"] == target_type
        assert node["target"]["swhid"].startswith(swhid_pattern)


@pytest.mark.parametrize(
    "filter_types, count",
    [
        ("revision, release", 2),
        ("revision, snapshot, release", 3),
    ],
)
def test_get_type_filter_multiple(client, filter_types, count):
    query_str = (
        """
    {
      snapshot(swhid: "swh:1:snp:0e7f84ede9a254f2cd55649ad5240783f557e65f") {
        branches(first:10, types: [%s]) {
          nodes {
            type
          }
        }
      }
    }"""
        % filter_types
    )
    data, _ = get_query_response(client, query_str)
    assert len(data["snapshot"]["branches"]["nodes"]) == count


@pytest.mark.parametrize("name", ["rel", "rev", "non-exist"])
def test_get_name_include_filter(client, name):
    query_str = (
        """
    {
      snapshot(swhid: "swh:1:snp:0e7f84ede9a254f2cd55649ad5240783f557e65f") {
        branches(first:10, nameInclude: "%s") {
          nodes {
            name {
              text
            }
          }
        }
      }
    }"""
        % name
    )
    data, _ = get_query_response(client, query_str)
    for node in data["snapshot"]["branches"]["nodes"]:
        assert name in node["name"]["text"]


@pytest.mark.parametrize("count", [1, 2])
def test_get_first_arg(client, count):
    query_str = (
        """
    {
      snapshot(swhid: "swh:1:snp:0e7f84ede9a254f2cd55649ad5240783f557e65f") {
        branches(first: %s) {
          nodes {
            type
          }
        }
      }
    }"""
        % count
    )
    data, _ = get_query_response(client, query_str)
    assert len(data["snapshot"]["branches"]["nodes"]) == count


def test_get_after_arg(client):
    query_str = """
    {
      snapshot(swhid: "swh:1:snp:0e7f84ede9a254f2cd55649ad5240783f557e65f") {
        branches(first: 1) {
          pageInfo {
            endCursor
          }
          nodes {
            name {
              text
            }
          }
        }
      }
    }"""
    first_data, _ = get_query_response(client, query_str)
    end_cursor = first_data["snapshot"]["branches"]["pageInfo"]["endCursor"]
    node_name = first_data["snapshot"]["branches"]["nodes"][0]["name"]["text"]

    query_str = (
        """
    {
      snapshot(swhid: "swh:1:snp:0e7f84ede9a254f2cd55649ad5240783f557e65f") {
        branches(first: 3, after: "%s") {
          nodes {
            type
            name {
              text
            }
          }
          edges {
            cursor
          }
        }
      }
    }"""
        % end_cursor
    )
    second_data, _ = get_query_response(client, query_str)
    branches = second_data["snapshot"]["branches"]
    assert len(branches["nodes"]) == 3
    assert branches["edges"][0]["cursor"] == end_cursor
    for node in branches["nodes"]:
        assert node["name"]["text"] > node_name
