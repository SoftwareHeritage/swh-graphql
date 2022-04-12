from .content import ContentNode
from .directory import DirectoryNode
from .directory_entry import DirectoryEntryConnection
from .origin import OriginConnection, OriginNode
from .release import BranchReleaseNode, ReleaseNode
from .revision import BranchRevisionNode, RevisionNode
from .snapshot import SnapshotNode, VisitSnapshotNode
from .snapshot_branch import SnapshotBranchConnection
from .visit import OriginVisitConnection, OriginVisitNode
from .visit_status import VisitStatusConnection

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
        "branch-revision": BranchRevisionNode,
        "branch-release": BranchReleaseNode,
        "revision": RevisionNode,
        "release": ReleaseNode,
        "directory": DirectoryNode,
        "content": ContentNode,
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
        "directory-entries": DirectoryEntryConnection,
    }
    # resolver_type = get_mapping_key(info) # FIXME, get full name
    if resolver_type not in mapping:
        raise AttributeError(f"Invalid type request {resolver_type}")
    return mapping[resolver_type]
