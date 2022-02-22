from ariadne import ObjectType

from . import query
from swh.graphql.backends import archive

origin = ObjectType("Origin")
origins = ObjectType("OriginConnection")


@query.field("origin")
def resolve_origin(_, info, **kw):
    """
    Top level query
    Get the origin matching the URL
    """
    # return BaseNode.factory('origin').get(filters)

    return archive.Archive().get_origins().results[0]


@origin.field("url")
def origin_url(origin, info):
    return origin.url


@origin.field("id")
def origin_id(origin, info):
    return origin.id.hex()


@query.field("origins")
def resolve_origins(_, info, **kw):
    """
    Top level query
    Get all the origins matching the criteria
    """
    # return BaseList.factory('origin').get(filters, state)

    origins = archive.Archive().get_origins(
        after=kw.get("after"), first=kw.get("first")
    )
    return origins


@origins.field("nodes")
def origin_nodes(origins, info, **kw):
    return origins.results


@origins.field("pageInfo")
def origin_pageinfo(origins, info, **kw):
    return {
        "hasNextPage": bool(origins.next_page_token),
        "endCursor": origins.next_page_token,
    }


@origin.field("visits")
def resolve_origin_visits(origin, info, **kw):
    return {
        "nodes": [
            {
                "id": "1",
                "status": "success"
            },
            {
                "id": "2",
                "status": "success"
            }
        ]
    }
