from ariadne import ObjectType

from . import query

origin = ObjectType("Origin")


@query.field("origin")
def resolve_origin(_, info, url):
    return {"url": "http://example.com"}


@origin.field("url")
def url(origin, info):
    return origin["url"]


@origin.field("visits")
def visits(origin, info):
    return [{"status": "success"}]
