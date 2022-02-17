from ariadne import ObjectType

from . import query
from ..backends import archive

origin = ObjectType("Origin")


@query.field("origin")
def resolve_origin(_, info, url):
    """
    """
    origin = archive.get_origin()
    return origin


@origin.field("url")
def url(origin, info):
    """
    """
    return origin["url"]


@origin.field("visits")
def visits(origin, info):
    """
    """
    return [{"status": "success"}]
