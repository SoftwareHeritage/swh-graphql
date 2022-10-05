# Copyright (C) 2022 The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information

import pytest

from swh.graphql import server
from swh.model.swhids import CoreSWHID, ObjectType

from . import utils
from ..data import get_directories, get_directories_with_nested_path


def get_target_type(target_type):
    mapping = {"file": "content", "dir": "directory", "rev": "revision"}
    return mapping.get(target_type)


def test_get_directory_entry_missing_path(client):
    directory = get_directories()[0]
    path = "missing"
    query_str = """
    query getDirEntry($swhid: SWHID!, $path: String!) {
      directoryEntry(directorySwhid: $swhid, path: $path) {
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
    """
    utils.assert_missing_object(
        client,
        query_str,
        "directoryEntry",
        swhid=str(directory.swhid()),
        path=path,
    )


@pytest.mark.parametrize(
    "directory", get_directories() + get_directories_with_nested_path()
)
def test_get_directory_entry(client, directory):
    storage = server.get_storage()
    query_str = """
    query getDirEntry($swhid: SWHID!, $path: String!) {
      directoryEntry(directorySwhid: $swhid, path: $path) {
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
        data, _ = utils.get_query_response(
            client,
            query_str,
            swhid=str(directory.swhid()),
            path=entry["name"].decode(),
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
            "targetType": get_target_type(entry["type"]),
        }


@pytest.mark.parametrize("directory", get_directories())
def test_get_directory_entry_connection(client, directory):
    query_str = """
    query getDirectory($swhid: SWHID!) {
      directory(swhid: $swhid) {
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
    data, _ = utils.get_query_response(client, query_str, swhid=str(directory.swhid()))
    directory_entries = data["directory"]["entries"]["nodes"]
    assert len(directory_entries) == len(directory.entries)
    output = [
        {"name": {"text": de.name.decode()}, "targetType": get_target_type(de.type)}
        for de in directory.entries
    ]
    for each_entry in output:
        assert each_entry in directory_entries


@pytest.mark.parametrize("directory", get_directories())
def test_directory_entry_connection_filter_by_name(client, directory):
    storage = server.get_storage()
    for dir_entry in storage.directory_ls(directory.id):
        name_include = dir_entry["name"][:-1].decode()
        query_str = """
        query getDirectory($swhid: SWHID!, $nameInclude: String) {
          directory(swhid: $swhid) {
            swhid
            entries(nameInclude: $nameInclude) {
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
        data, _ = utils.get_query_response(
            client,
            query_str,
            swhid=str(directory.swhid()),
            nameInclude=name_include,
        )
        for entry in data["directory"]["entries"]["nodes"]:
            assert name_include in entry["name"]["text"]
            assert entry["targetType"] == get_target_type(dir_entry["type"])
