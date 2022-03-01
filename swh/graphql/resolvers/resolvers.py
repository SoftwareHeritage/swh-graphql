from .origin import OriginConnection, OriginNode
from .visit import OriginVisitConnection

from ariadne import ObjectType

query = ObjectType("Query")
origin = ObjectType("Origin")
origins = ObjectType("OriginConnection")
visit = ObjectType("Visit")


def get_node_resolver(resolver_type):
    # FIXME, replace with a proper factory method
    mapping = {
        "origin": OriginNode,
    }
    if resolver_type not in mapping:
        raise AttributeError("Invalid type request")
    return mapping[resolver_type]


def get_connection_resolver(resolver_type):
    # FIXME, replace with a proper factory method
    mapping = {"origins": OriginConnection, "origin_visits": OriginVisitConnection}
    if resolver_type not in mapping:
        raise AttributeError("Invalid type request")
    return mapping[resolver_type]


# Nodes


@query.field("origin")
def node_resolver(obj, info, **kw):
    """
    Resolver for all the node types
    """
    # FIXME change to static factory in base class
    resolver = get_node_resolver(info.field_name)
    return resolver(obj, info, **kw)()


# Resolvers for node fields
# Safer to annotate them here than adding as
# property in the node class


@origin.field("id")
def origin_id(origin, info):
    # Using ariadne decorator to avoid infinite loop issue with id
    return origin.id.hex()


@visit.field("date")
def visit_date(visit, info):
    return visit.date.timestamp()


@visit.field("id")
def visit_id(visit, info):
    return str(visit.visit)


# Connections


@origin.field("visits")
@query.field("origins")
def connection_resolver(obj, info, **kw):
    # FIXME change to static factory in base class
    resolver = get_connection_resolver(info.field_name)
    return resolver(obj, info, **kw)()


# Other
