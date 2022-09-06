# Copyright (C) 2022 The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information

import pytest

from swh.graphql import server
from swh.model.swhids import CoreSWHID, ObjectType

from . import utils
from ..data import get_directories, get_directories_with_nested_path


def test_get_directory_entry_missing_path(client):
    directory = get_directories()[0]
    path = "missing"
    query_str = """
    {
      directoryEntry(swhid: "%s", path: "%s") {
        name {
          text
        }
        targetType
        target {
          ...on Content {
            swhid
          }
        }
      }
    }
    """ % (
        directory.swhid(),
        path,
    )
    utils.assert_missing_object(client, query_str, "directoryEntry")


@pytest.mark.parametrize(
    "directory", get_directories() + get_directories_with_nested_path()
)
def test_get_directory_entry(client, directory):
    storage = server.get_storage()
    query_str = """
    {
      directoryEntry(swhid: "%s", path: "%s") {
        name {
          text
        }
        targetType
        target {
          ...on Content {
            swhid
          }
          ...on Directory {
            swhid
          }
          ...on Revision {
            swhid
          }
        }
      }
    }
    """
    for entry in storage.directory_ls(directory.id, recursive=True):
        query = query_str % (
            directory.swhid(),
            entry["name"].decode(),
        )
        data, _ = utils.get_query_response(
            client,
            query,
        )
        swhid = None
        if entry["type"] == "file" and entry["sha1_git"] is not None:
            swhid = CoreSWHID(
                object_type=ObjectType.CONTENT, object_id=entry["sha1_git"]
            )
        elif entry["type"] == "dir" and entry["target"] is not None:
            swhid = CoreSWHID(
                object_type=ObjectType.DIRECTORY, object_id=entry["target"]
            )
        elif entry["type"] == "rev" and entry["target"] is not None:
            swhid = CoreSWHID(
                object_type=ObjectType.REVISION, object_id=entry["target"]
            )
        assert data["directoryEntry"] == {
            "name": {"text": entry["name"].decode()},
            "target": {"swhid": str(swhid)} if swhid else None,
            "targetType": entry["type"],
        }


@pytest.mark.parametrize("directory", get_directories())
def test_get_directory_entry_connection(client, directory):
    query_str = """
    {
      directory(swhid: "%s") {
        swhid
        entries {
          nodes {
            targetType
            name {
              text
            }
          }
        }
      }
    }
    """
    data, _ = utils.get_query_response(client, query_str % directory.swhid())
    directory_entries = data["directory"]["entries"]["nodes"]
    assert len(directory_entries) == len(directory.entries)
    output = [
        {"name": {"text": de.name.decode()}, "targetType": de.type}
        for de in directory.entries
    ]
    for each_entry in output:
        assert each_entry in directory_entries
