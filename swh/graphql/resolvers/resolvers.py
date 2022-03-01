from .origin import OriginConnection, OriginNode
from .visit import OriginVisitConnection

from ariadne import ObjectType

query = ObjectType("Query")
origin = ObjectType("Origin")
origins = ObjectType("OriginConnection")
visit = ObjectType("Visit")


def node_resolver_factory(resolver_type, obj, info, **kw):
    mapping = {
        "origin": OriginNode,
    }
    return mapping[resolver_type](obj, info, **kw)


def connection_resolver_factory(resolver_type, obj, info, **kw):
    mapping = {
        "origins": OriginConnection,
        "origin_visits": OriginVisitConnection
    }
    return mapping[resolver_type](obj, info, **kw)


# Nodes

@query.field("origin")
def resolve_origin(_, info, **kw):
    """
    Top level query
    Get the origin matching the URL
    """

    # FIXME change to static factory in base class to avoid args
    return node_resolver_factory("origin", None, info, **kw)()


@origin.field("id")
def origin_id(origin, info):
    # Using ariadne decorator to avoid infinite loop issue with id
    return origin.id.hex()


# def resolve_visit(_, info, **kw):
#     pass

@visit.field("date")
def visit_date(visit, info):
    return visit.date.timestamp()


@visit.field("id")
def visit_id(visit, info):
    return str(visit.visit)


# Connections


@query.field("origins")
def resolve_origins(_, info, **kw):
    # FIXME change to static factory in base class
    return connection_resolver_factory("origins", None, info, **kw)()


@origin.field("visits")
def origin_visits(origin, info, **kw):
    return connection_resolver_factory("origin_visits", origin, info, **kw)()

@visit.field("status")
def origin_visits(origin, info, **kw):
    return connection_resolver_factory("origin_visits", origin, info, **kw)()

# Other
