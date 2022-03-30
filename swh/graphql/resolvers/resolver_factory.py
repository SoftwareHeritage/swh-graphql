from .origin import OriginConnection, OriginNode
from .snapshot import SnapshotNode, VisitSnapshotNode
from .snapshot_branch import SnapshotBranchConnection
from .visit import OriginVisitConnection, OriginVisitNode
from .visit_status import VisitStatusConnection


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
        "snapshot-branches": SnapshotBranchConnection,
    }
    # resolver_type = get_mapping_key(info) # FIXME, get full name
    if resolver_type not in mapping:
        raise AttributeError(f"Invalid type request {resolver_type}")
    return mapping[resolver_type]
