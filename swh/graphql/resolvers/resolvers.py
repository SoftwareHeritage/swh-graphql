"""
High level resolvers
Any schema attribute can be resolved by any of the following ways
and in the following priority order
- In this module using an annotation  (eg: @visitstatus.field("snapshot"))
- As a property in the model object (eg: models.visit.VisitModel.id)
- As an attribute/item in the object/dict returned by the backend (eg: Origin.url)
"""
from ariadne import ObjectType, UnionType

from .resolver_factory import get_connection_resolver, get_node_resolver

query = ObjectType("Query")
origin = ObjectType("Origin")
origins = ObjectType("OriginConnection")
visit = ObjectType("Visit")
visitstatus = ObjectType("VisitStatus")
snapshot = ObjectType("Snapshot")
branch = ObjectType("Branch")
target = UnionType("BranchTarget")

# Node resolvers
# A node resolver can return a model object or a data structure


@query.field("origin")
def origin_resolver(obj, info, **kw):
    """
    """
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


@branch.field("target")
def branch_target(obj, info, **kw):
    """
    Branch target can be a revision or a release
    """
    resolver_type = obj.type
    resolver = get_node_resolver(resolver_type)
    return resolver(obj, info, **kw)()


# Connection resolvers
# A connection resolver will return a sub class of BaseConnection


@query.field("origins")
def origins_resolver(obj, info, **kw):
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


# Any other type of resolver


@target.type_resolver
def union_resolver(obj, *_):
    """
    To resolve any union type
    """
    return obj.is_type_of()
