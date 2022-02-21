from ariadne import ObjectType

from . import query
from swh.graphql.backends import archive

origin = ObjectType("Origin")
originSearch = ObjectType("OriginConnection")


@query.field("origin")
def resolve_origin(_, info, url):
    """
    Top level query
    Get the origin matching the URL
    """
    origin = archive.get_origins()
    return origin[0]


@origin.field("url")
def origin_url(origin, info):
    return origin.url


@query.field("origins")
def resolve_origin_search(_, info, **kw):
    """
    Top level query
    Get all the origins matching the criteria
    """
    # return BaseList.factory('origin').get(filters, state)

    return archive.get_origins()


@originSearch.field("nodes")
def origin_nodes(origins, info, **kw):
    return origins


@originSearch.field("pageInfo")
def origin_pageinfo(origins, info, **kw):
    return {"hasNextPage": True, "hasPreviousPage": True}
