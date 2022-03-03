# FIXME, get rid of this module by directly decorating node/connection classes
from ariadne import ObjectType

from swh.graphql.utils import utils

from .origin import OriginConnection, OriginNode
from .visit import OriginVisitNode, OriginVisitConnection, VisitStatusConnection
from .snapshot import VisitSnapshotNode, SnapshotNode

query = ObjectType("Query")
origin = ObjectType("Origin")
origins = ObjectType("OriginConnection")
visit = ObjectType("Visit")
visitstatus = ObjectType("VisitStatus")
snapshot = ObjectType("Snapshot")

# def get_mapping_key(info):
#     """
#     Logic to resolve mapping type
#     """
#     # FIXME, move to utils
#     if info.path.prev:
#         return f"{info.path.prev.key}_{info.path.key}"
#     return info.path.key


def get_node_resolver(resolver_type):
    # FIXME, replace with a proper factory method
    mapping = {
        "origin": OriginNode,
        "visit": OriginVisitNode,
        "visit-snapshot": VisitSnapshotNode,
        "snapshot": SnapshotNode,
    }
    # resolver_type = get_mapping_key(info) # FIXME, get full name
    if resolver_type not in mapping:
        raise AttributeError(f"Invalid type request {resolver_type}")
    return mapping[resolver_type]


def get_connection_resolver(resolver_type):
    # FIXME, replace with a proper factory method
    mapping = {
        "origins": OriginConnection,
        "origin-visits": OriginVisitConnection,
        "visit-status": VisitStatusConnection,
    }
    # resolver_type = get_mapping_key(info) # FIXME, get full name
    if resolver_type not in mapping:
        raise AttributeError(f"Invalid type request {resolver_type}")
    return mapping[resolver_type]


# Nodes


@query.field("origin")
def origin_resolver(obj, info, **kw):
    """
    """
    # FIXME change to static factory in base class
    resolver = get_node_resolver("origin")
    return resolver(obj, info, **kw)()


@query.field("visit")
def visit_resolver(obj, info, **kw):
    """
    """
    resolver = get_node_resolver("visit")
    return resolver(obj, info, **kw)()


@query.field("snapshot")
def snapshot_resolver(obj, info, **kw):
    """
    """
    resolver = get_node_resolver("snapshot")
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
    # FIXME, find a proper id
    return utils.encode("temp-id")


@visitstatus.field("snapshot")
def visit_snapshot(obj, info, **kw):
    resolver = get_node_resolver("visit-snapshot")
    return resolver(obj, info, **kw)()


# Connections


@query.field("origins")
def origins_resolver(obj, info, **kw):
    # FIXME change to static factory in base class
    resolver = get_connection_resolver("origins")
    return resolver(obj, info, **kw)()


@origin.field("visits")
def visits_resolver(obj, info, **kw):
    resolver = get_connection_resolver("origin-visits")
    return resolver(obj, info, **kw)()


@visit.field("status")
def visitstatus_resolver(obj, info, **kw):
    resolver = get_connection_resolver("visit-status")
    return resolver(obj, info, **kw)()


# Other
