# Copyright (C) 2022 The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information

import pytest

from swh.graphql import server


def test_get_storage(mocker):
    server.storage = None
    server.graphql_cfg = {"storage": {"test": "test"}}
    mocker.patch("swh.graphql.server.get_swh_storage", return_value="dummy-storage")
    assert server.get_storage() == "dummy-storage"


def test_get_global_storage(mocker):
    server.storage = "existing-storage"
    assert server.get_storage() == "existing-storage"


def test_get_search(mocker):
    server.search = None
    server.graphql_cfg = {"search": {"test": "test"}}
    mocker.patch("swh.graphql.server.get_swh_search", return_value="dummy-search")
    assert server.get_search() == "dummy-search"


def test_get_global_search(mocker):
    server.search = "existing-search"
    assert server.get_search() == "existing-search"


def test_load_and_check_config_no_config():
    with pytest.raises(EnvironmentError):
        server.load_and_check_config(config_path=None)


def test_load_and_check_config_missing_config_file():
    with pytest.raises(FileNotFoundError):
        server.load_and_check_config(config_path="invalid")


def test_load_and_check_config_missing_storage_config(mocker):
    mocker.patch("swh.core.config.read", return_value={"test": "test"})
    with pytest.raises(KeyError):
        server.load_and_check_config(config_path="/tmp")


def test_load_and_check_config(mocker):
    mocker.patch("swh.core.config.read", return_value={"storage": {"test": "test"}})
    cfg = server.load_and_check_config(config_path="/tmp")
    assert cfg == {"storage": {"test": "test"}}


def test_make_app_from_configfile_with_config(mocker):
    server.graphql_cfg = {
        "storage": {"test": "test"},
        "debug": True,
        "introspection": True,
    }
    mocker.patch("starlette.middleware.cors.CORSMiddleware", return_value="dummy-app")
    assert server.make_app_from_configfile() == "dummy-app"


def test_make_app_from_configfile_missing_config(mocker):
    server.graphql_cfg = None
    with pytest.raises(EnvironmentError):
        # trying to load config from a non existing env var
        assert server.make_app_from_configfile()
