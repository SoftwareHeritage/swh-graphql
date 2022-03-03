from ariadne import ObjectType

from swh.graphql.utils import utils

from .origin import OriginConnection, OriginNode
from .visit import OriginVisit, OriginVisitConnection, VisitStatusConnection

query = ObjectType("Query")
origin = ObjectType("Origin")
origins = ObjectType("OriginConnection")
visit = ObjectType("Visit")
visitstatus = ObjectType("VisitStatus")


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
    mapping = {
        "origins": OriginConnection,
        "visits": OriginVisitConnection,
        "status": VisitStatusConnection,
    }
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
# Using ariadne resolution instead of adding properties in Node
# That is to avoid looping in NodeConnection


@visit.field("id")
def visit_id(visit, info):
    # FIXME, find a better id for visit
    return utils.encode(f"{visit.origin}-{str(visit.visit)}")


@visitstatus.field("id")
def visit_status_id(_, info):
    # FIXME, find a better id
    return utils.encode("temp-id")


@visitstatus.field("snapshot")
def visit_status_id(status, info, **kw):
    # return SnapshotNode()
    return status.snapshot.hex()


# Connections


@visit.field("status")
@origin.field("visits")
@query.field("origins")
def connection_resolver(obj, info, **kw):
    # FIXME change to static factory in base class
    resolver = get_connection_resolver(info)
    return resolver(obj, info, **kw)()


# Other
