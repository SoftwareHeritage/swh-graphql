# Copyright (C) 2022 The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information

import os
from typing import Any, Dict, Optional

from swh.core import config
from swh.search import get_search as get_swh_search
from swh.storage import get_storage as get_swh_storage

graphql_cfg = None
storage = None
search = None


def get_storage():
    global storage
    if not storage:
        storage = get_swh_storage(**graphql_cfg["storage"])
    return storage


def get_search():
    global search
    if not search:
        search = get_swh_search(**graphql_cfg["search"])
    return search


def load_and_check_config(config_path: Optional[str]) -> Dict[str, Any]:
    """Check the minimal configuration is set to run the api or raise an
       error explanation.

    Args:
        config_path: Path to the configuration file to load

    Raises:
        Error if the setup is not as expected

    Returns:
        configuration as a dict

    """
    if not config_path:
        raise EnvironmentError("Configuration file must be defined")

    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Configuration file {config_path} does not exist")

    cfg = config.read(config_path)
    if "storage" not in cfg:
        raise KeyError("Missing 'storage' configuration")

    return cfg


def make_app_from_configfile():
    """Loading the configuration from a configuration file.

    SWH_CONFIG_FILENAME environment variable defines the
    configuration path to load.
    """
    from .app import schema
    from .errors.handlers import format_error

    global graphql_cfg

    if not graphql_cfg:
        config_path = os.environ.get("SWH_CONFIG_FILENAME")
        graphql_cfg = load_and_check_config(config_path)

    server_type = graphql_cfg.get("server-type")
    if server_type == "asgi":
        from ariadne.asgi import GraphQL
        from starlette.middleware.cors import CORSMiddleware

        # Enable cors in the asgi version
        application = CORSMiddleware(
            GraphQL(schema, debug=graphql_cfg["debug"], error_formatter=format_error),
            allow_origins=["*"],
            allow_methods=("GET", "POST", "OPTIONS"),
        )
    else:
        from ariadne.wsgi import GraphQL

        application = GraphQL(
            schema, debug=graphql_cfg["debug"], error_formatter=format_error
        )
    return application
