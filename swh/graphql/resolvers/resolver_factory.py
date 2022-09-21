# Copyright (C) 2022 The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information

from typing import ClassVar, Dict, Type

from swh.graphql.errors import NullableObjectError

from .base_connection import BaseConnection
from .base_node import BaseNode
from .content import ContentNode, HashContentNode, TargetContentNode
from .directory import DirectoryNode, RevisionDirectoryNode, TargetDirectoryNode
from .directory_entry import DirectoryEntryConnection, DirectoryEntryNode
from .origin import OriginConnection, OriginNode, TargetOriginNode
from .release import ReleaseNode, TargetReleaseNode
from .revision import (
    LogRevisionConnection,
    ParentRevisionConnection,
    RevisionNode,
    TargetRevisionNode,
)
from .search import ResolveSwhidConnection, SearchConnection
from .snapshot import (
    OriginSnapshotConnection,
    SnapshotNode,
    TargetSnapshotNode,
    VisitSnapshotNode,
)
from .snapshot_branch import AliasSnapshotBranchNode, SnapshotBranchConnection
from .visit import LatestVisitNode, OriginVisitConnection, OriginVisitNode
from .visit_status import LatestVisitStatusNode, VisitStatusConnection


class NodeObjectFactory:
    mapping: ClassVar[Dict[str, Type[BaseNode]]] = {
        "origin": OriginNode,
        "visit": OriginVisitNode,
        "latest-visit": LatestVisitNode,
        "latest-status": LatestVisitStatusNode,
        "visit-snapshot": VisitSnapshotNode,
        "snapshot": SnapshotNode,
        "branch-alias": AliasSnapshotBranchNode,
        "branch-revision": TargetRevisionNode,
        "branch-release": TargetReleaseNode,
        "branch-directory": TargetDirectoryNode,
        "branch-content": TargetContentNode,
        "branch-snapshot": TargetSnapshotNode,
        "revision": RevisionNode,
        "revision-directory": RevisionDirectoryNode,
        "release": ReleaseNode,
        "release-revision": TargetRevisionNode,
        "release-release": TargetReleaseNode,
        "release-directory": TargetDirectoryNode,
        "release-content": TargetContentNode,
        "directory": DirectoryNode,
        "directory-entry": DirectoryEntryNode,
        "content": ContentNode,
        "content-by-hash": HashContentNode,
        "dir-entry-content": TargetContentNode,
        "dir-entry-directory": TargetDirectoryNode,
        "dir-entry-revision": TargetRevisionNode,
        "search-result-origin": TargetOriginNode,
        "search-result-snapshot": TargetSnapshotNode,
        "search-result-revision": TargetRevisionNode,
        "search-result-release": TargetReleaseNode,
        "search-result-directory": TargetDirectoryNode,
        "search-result-content": TargetContentNode,
    }

    @classmethod
    def create(cls, node_type: str, obj, info, *args, **kw):
        resolver = cls.mapping.get(node_type)
        if not resolver:
            raise AttributeError(f"Invalid node type: {node_type}")
        try:
            node_obj = resolver(obj, info, *args, **kw)
        except NullableObjectError:
            # Return None instead of the object
            node_obj = None
        return node_obj


class ConnectionObjectFactory:
    mapping: ClassVar[Dict[str, Type[BaseConnection]]] = {
        "origins": OriginConnection,
        "origin-visits": OriginVisitConnection,
        "origin-snapshots": OriginSnapshotConnection,
        "visit-status": VisitStatusConnection,
        "snapshot-branches": SnapshotBranchConnection,
        "revision-parents": ParentRevisionConnection,
        "revision-log": LogRevisionConnection,
        "directory-entries": DirectoryEntryConnection,
        "resolve-swhid": ResolveSwhidConnection,
        "search": SearchConnection,
    }

    @classmethod
    def create(cls, connection_type: str, obj, info, *args, **kw):
        resolver = cls.mapping.get(connection_type)
        if not resolver:
            raise AttributeError(f"Invalid connection type: {connection_type}")
        return resolver(obj, info, *args, **kw)
