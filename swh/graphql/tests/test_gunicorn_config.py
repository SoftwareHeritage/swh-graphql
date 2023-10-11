# Copyright (C) 2023  The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information

import os

import swh.graphql.gunicorn_config as gunicorn_config


def test_post_fork_default(mocker):
    sentry_sdk_init = mocker.patch("sentry_sdk.init")

    gunicorn_config.post_fork(None, None)

    sentry_sdk_init.assert_not_called()


def test_post_fork_with_dsn_env(mocker):
    ariadne_integration = object()  # unique object to check for equality
    mocker.patch(
        "swh.graphql.gunicorn_config.AriadneIntegration",
        new=lambda: ariadne_integration,
    )
    sentry_sdk_init = mocker.patch("sentry_sdk.init")
    mocker.patch.dict(os.environ, {"SWH_SENTRY_DSN": "test_dsn"})

    gunicorn_config.post_fork(None, None)

    sentry_sdk_init.assert_called_once_with(
        dsn="test_dsn",
        environment=None,
        integrations=[ariadne_integration],
        debug=False,
        release=None,
        send_default_pii=True,
    )


def test_post_fork_debug(mocker):
    ariadne_integration = object()  # unique object to check for equality
    mocker.patch(
        "swh.graphql.gunicorn_config.AriadneIntegration",
        new=lambda: ariadne_integration,
    )
    sentry_sdk_init = mocker.patch("sentry_sdk.init")
    mocker.patch.dict(
        os.environ, {"SWH_SENTRY_DSN": "test_dsn", "SWH_SENTRY_DEBUG": "1"}
    )

    gunicorn_config.post_fork(None, None)

    sentry_sdk_init.assert_called_once_with(
        dsn="test_dsn",
        environment=None,
        integrations=[ariadne_integration],
        debug=True,
        release=None,
        send_default_pii=True,
    )
