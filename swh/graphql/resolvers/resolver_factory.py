from .content import ContentNode, TargetContentNode
from .directory import DirectoryNode, RevisionDirectoryNode, TargetDirectoryNode
from .directory_entry import DirectoryEntryConnection
from .origin import OriginConnection, OriginNode
from .release import ReleaseNode, TargetReleaseNode
from .revision import ParentRevisionConnection, RevisionNode, TargetRevisionNode
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
        "branch-revision": TargetRevisionNode,
        "release-revision": TargetRevisionNode,
        "branch-release": TargetReleaseNode,
        "release-release": TargetReleaseNode,
        "release-directory": TargetDirectoryNode,
        "release-content": TargetContentNode,
        "revision": RevisionNode,
        "revision-directory": RevisionDirectoryNode,
        "release": ReleaseNode,
        "directory": DirectoryNode,
        "content": ContentNode,
        "dir-entry-dir": TargetDirectoryNode,
        "dir-entry-file": TargetContentNode,
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
        "revision-parents": ParentRevisionConnection,
        "directory-entries": DirectoryEntryConnection,
        # revision-parents
    }
    # resolver_type = get_mapping_key(info) # FIXME, get full name
    if resolver_type not in mapping:
        raise AttributeError(f"Invalid type request {resolver_type}")
    return mapping[resolver_type]
