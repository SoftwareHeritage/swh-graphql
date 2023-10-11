# Copyright (C) 2023  The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information

from sentry_sdk.integrations.ariadne import AriadneIntegration

from swh.core.sentry import init_sentry


def post_fork(server, worker):
    init_sentry(
        sentry_dsn=None,  # set through SWH_SENTRY_DSN environment variable
        integrations=[AriadneIntegration()],
        extra_kwargs={
            # required to include GraphQL requests and responses data in sentry reports
            "send_default_pii": True
        },
    )
