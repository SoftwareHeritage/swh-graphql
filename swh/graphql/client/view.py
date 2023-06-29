# Copyright (C) 2023 The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information

import os
from urllib.request import urlopen

from starlette.templating import Jinja2Templates


def get_query(query_url=None):
    # FIXME hack to make sharing a query easy
    # can be removed after the SWH-explorer client app

    # read from SWH gitlab snippets
    # this is safe as we support only GET at the moment

    query_url = (
        "https://gitlab.softwareheritage.org/-/snippets/1580/raw/main/snippetfile1.txt"
    )
    f = urlopen(query_url)
    # if query_url is None or not query_url.startswith(""):
    #     return ""
    # return f.read().decode()
    # default_query = """ """
    query = f.read().decode().replace("\n", "").replace("\t", "")
    return query
    # return "query getDir { origins(first: 1) { nodes {  url  }  } }"


async def explorer_page(request):
    from swh.graphql.server import graphql_cfg

    auth = graphql_cfg.get("auth")
    if auth and "public_server" not in auth:
        # ensure to not break already deployed service
        auth["public_server"] = auth["server"]

    templates = Jinja2Templates(directory=os.path.dirname(__file__))
    query = get_query()
    return templates.TemplateResponse(
        "explorer.html", {"request": request, "auth": auth, "query": query}
    )
