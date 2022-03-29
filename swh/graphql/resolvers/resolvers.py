# FIXME, get rid of this module by directly decorating node/connection classes
# High level resolvers
from ariadne import ObjectType

from .resolver_factory import get_connection_resolver, get_node_resolver

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

# Node resolvers


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


@snapshot.field("branches")
def snapshot_branches(obj, info, **kw):
    resolver = get_connection_resolver("snapshot-branches")
    return resolver(obj, info, **kw)()


# Other
