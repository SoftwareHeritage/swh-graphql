from ariadne import ObjectType

from swh.graphql.utils import utils

from .origin import OriginConnection, OriginNode
from .visit import OriginVisit, OriginVisitConnection

query = ObjectType("Query")
origin = ObjectType("Origin")
origins = ObjectType("OriginConnection")
visit = ObjectType("Visit")


def get_mapping_key(info):
    """
    Logic to resolve mapping type
    """
    # FIXME, move to utils
    if info.path.prev:
        return f"{info.path.prev.key}_{info.path.key}"
    return info.path.key


def get_node_resolver(info):
    # FIXME, replace with a proper factory method
    mapping = {"origin": OriginNode, "visit": OriginVisit}
    resolver_type = info.path.key  # get_mapping_key(info) # FIXME, get full name
    if resolver_type not in mapping:
        raise AttributeError(f"Invalid type request {resolver_type}")
    return mapping[resolver_type]


def get_connection_resolver(info):
    # FIXME, replace with a proper factory method
    mapping = {"origins": OriginConnection, "visits": OriginVisitConnection}
    resolver_type = info.path.key  # get_mapping_key(info)  # FIXME, get full name
    if resolver_type not in mapping:
        raise AttributeError(f"Invalid type request {resolver_type}")
    return mapping[resolver_type]


# Nodes


@query.field("visit")
@query.field("origin")
def node_resolver(obj, info, **kw):
    """
    Resolver for all the node types
    """
    # FIXME change to static factory in base class
    resolver = get_node_resolver(info)
    return resolver(obj, info, **kw)()


# Resolvers for node fields
# Safer to annotate them here than adding as
# property in the node class


@origin.field("id")
def origin_id(origin, info):
    # Using ariadne decorator to avoid infinite loop issue with id
    return origin.id.hex()


@visit.field("id")
def visit_id(visit, info):
    # FIXME, find a better id for visit
    return utils.encode(f"{visit.origin}-{str(visit.visit)}")


# Connections


@origin.field("visits")
@query.field("origins")
def connection_resolver(obj, info, **kw):
    # FIXME change to static factory in base class
    resolver = get_connection_resolver(info)
    return resolver(obj, info, **kw)()


# Other
