from ariadne import ObjectType

from . import query
from swh.graphql.backends import archive

origin = ObjectType("Origin")


@query.field("origin")
def resolve_origin(_, info, url):
    """
    """
    origin = archive.get_origins()
    return origin[0]


@origin.field("url")
def url(origin, info):
    """
    """
    # return origin.url
    return origin["url"]


@origin.field("visits")
def visits(origin, info):
    """
    """
    return [{"status": "success"}]
