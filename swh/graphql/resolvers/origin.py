from ariadne import ObjectType

from . import query
from swh.graphql.backends import archive

origin = ObjectType("Origin")
origins = ObjectType("OriginConnection")

visit = ObjectType("Visit")


@query.field("origin")
def resolve_origin(_, info, **kw):
    """
    Top level query
    Get the origin matching the URL
    """
    # return BaseNode.factory('origin').get(filters)

    return archive.Archive().get_origin(kw["url"])


# @origin.field("url")
# def origin_url(origin, info):
#     return origin.url


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
    # return results

    return {
        "nodes": origins.results,
        "pageInfo": {
            "hasNextPage": bool(origins.next_page_token),
            "endCursor": origins.next_page_token,
        },
    }


@origin.field("visits")
def resolve_origin_visits(origin, info, **kw):
    visits = archive.Archive().get_origin_visits(
        origin.url, after=kw.get("after"), first=kw.get("first")
    )
    return {
        "nodes": visits.results,
        "pageInfo": {
            "hasNextPage": bool(visits.next_page_token),
            "endCursor": visits.next_page_token,
        },
    }


@visit.field("status")
def visit_status(visit, info):
    return str(visit.visit)


@visit.field("date")
def visit_date(visit, info):
    return visit.date.timestamp()
