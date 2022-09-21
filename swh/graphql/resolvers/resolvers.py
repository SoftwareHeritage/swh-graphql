# Copyright (C) 2022 The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information

"""
High level resolvers
"""

# Any schema attribute can be resolved by any of the following ways
# and in the following priority order
# - In this module using a decorator (eg: @visit_status.field("snapshot"))
#   Every object (type) is expected to resolve this way as they can accept arguments
#   eg: origin.visits takes arguments to paginate
# - As a property in the Node object (eg: resolvers.visit.BaseVisitNode.id)
#   Every scalar is expected to resolve this way
# - As an attribute/item in the object/dict returned by a backend (eg: Origin.url)

from typing import Optional, Union

from ariadne import ObjectType, UnionType
from graphql.type import GraphQLResolveInfo

from swh.graphql import resolvers as rs
from swh.graphql.utils import utils

from .resolver_factory import ConnectionObjectFactory, NodeObjectFactory

query: ObjectType = ObjectType("Query")
origin: ObjectType = ObjectType("Origin")
visit: ObjectType = ObjectType("Visit")
visit_status: ObjectType = ObjectType("VisitStatus")
snapshot: ObjectType = ObjectType("Snapshot")
snapshot_branch: ObjectType = ObjectType("Branch")
revision: ObjectType = ObjectType("Revision")
release: ObjectType = ObjectType("Release")
directory: ObjectType = ObjectType("Directory")
directory_entry: ObjectType = ObjectType("DirectoryEntry")
search_result: ObjectType = ObjectType("SearchResult")
binary_string: ObjectType = ObjectType("BinaryString")

branch_target: UnionType = UnionType("BranchTarget")
release_target: UnionType = UnionType("ReleaseTarget")
directory_entry_target: UnionType = UnionType("DirectoryEntryTarget")
search_result_target: UnionType = UnionType("SearchResultTarget")

# Node resolvers
# A node resolver will return either an instance of a BaseNode subclass or None


@query.field("origin")
def origin_resolver(obj: None, info: GraphQLResolveInfo, **kw) -> rs.origin.OriginNode:
    return NodeObjectFactory.create("origin", obj, info, **kw)


@origin.field("latestVisit")
def latest_visit_resolver(
    obj: rs.origin.BaseOriginNode, info: GraphQLResolveInfo, **kw
) -> Optional[rs.visit.LatestVisitNode]:
    return NodeObjectFactory.create("latest-visit", obj, info, **kw)


@query.field("visit")
def visit_resolver(
    obj: None, info: GraphQLResolveInfo, **kw
) -> rs.visit.OriginVisitNode:
    return NodeObjectFactory.create("visit", obj, info, **kw)


@visit.field("latestStatus")
def latest_visit_status_resolver(
    obj: rs.visit.BaseVisitNode, info: GraphQLResolveInfo, **kw
) -> Optional[rs.visit_status.LatestVisitStatusNode]:
    return NodeObjectFactory.create("latest-status", obj, info, **kw)


@query.field("snapshot")
def snapshot_resolver(
    obj: None, info: GraphQLResolveInfo, **kw
) -> rs.snapshot.SnapshotNode:
    return NodeObjectFactory.create("snapshot", obj, info, **kw)


@visit_status.field("snapshot")
def visit_snapshot_resolver(
    obj: rs.visit_status.BaseVisitStatusNode, info: GraphQLResolveInfo, **kw
) -> Optional[rs.snapshot.VisitSnapshotNode]:
    return NodeObjectFactory.create("visit-snapshot", obj, info, **kw)


@snapshot_branch.field("target")
def snapshot_branch_target_resolver(
    obj: rs.snapshot_branch.BaseSnapshotBranchNode, info: GraphQLResolveInfo, **kw
) -> Union[
    rs.revision.BaseRevisionNode,
    rs.release.BaseReleaseNode,
    rs.directory.BaseDirectoryNode,
    rs.content.BaseContentNode,
    rs.snapshot.BaseSnapshotNode,
    rs.snapshot_branch.BaseSnapshotBranchNode,
]:
    """
    Snapshot branch target can be a revision, release, directory,
    content, snapshot or a branch itself (alias type)
    """
    return NodeObjectFactory.create(f"branch-{obj.targetType}", obj, info, **kw)


@query.field("revision")
def revision_resolver(
    obj: None, info: GraphQLResolveInfo, **kw
) -> rs.revision.RevisionNode:
    return NodeObjectFactory.create("revision", obj, info, **kw)


@revision.field("directory")
def revision_directory_resolver(
    obj: rs.revision.BaseRevisionNode, info: GraphQLResolveInfo, **kw
) -> Optional[rs.directory.RevisionDirectoryNode]:
    return NodeObjectFactory.create("revision-directory", obj, info, **kw)


@query.field("release")
def release_resolver(
    obj: None, info: GraphQLResolveInfo, **kw
) -> rs.release.ReleaseNode:
    return NodeObjectFactory.create("release", obj, info, **kw)


@release.field("target")
def release_target_resolver(
    obj: rs.release.BaseReleaseNode, info: GraphQLResolveInfo, **kw
) -> Union[
    rs.revision.BaseRevisionNode,
    rs.release.BaseReleaseNode,
    rs.directory.BaseDirectoryNode,
    rs.content.BaseContentNode,
]:
    """
    Release target can be a release, revision, directory or a content
    """
    return NodeObjectFactory.create(f"release-{obj.targetType}", obj, info, **kw)


@query.field("directory")
def directory_resolver(
    obj: None, info: GraphQLResolveInfo, **kw
) -> rs.directory.DirectoryNode:
    return NodeObjectFactory.create("directory", obj, info, **kw)


@query.field("directoryEntry")
def directory_entry_resolver(
    obj: None, info: GraphQLResolveInfo, **kw
) -> rs.directory_entry.DirectoryEntryNode:
    return NodeObjectFactory.create("directory-entry", obj, info, **kw)


@directory_entry.field("target")
def directory_entry_target_resolver(
    obj: rs.directory_entry.BaseDirectoryEntryNode, info: GraphQLResolveInfo, **kw
) -> Union[
    rs.revision.BaseRevisionNode,
    rs.directory.BaseDirectoryNode,
    rs.content.BaseContentNode,
]:
    """
    DirectoryEntry target can be a directory, content or a revision
    """
    return NodeObjectFactory.create(f"dir-entry-{obj.targetType}", obj, info, **kw)


@query.field("content")
def content_resolver(
    obj: None, info: GraphQLResolveInfo, **kw
) -> rs.content.ContentNode:
    return NodeObjectFactory.create("content", obj, info, **kw)


@search_result.field("target")
def search_result_target_resolver(
    obj: rs.search.SearchResultNode, info: GraphQLResolveInfo, **kw
) -> Union[
    rs.origin.BaseOriginNode,
    rs.snapshot.BaseSnapshotNode,
    rs.revision.BaseRevisionNode,
    rs.release.BaseReleaseNode,
    rs.directory.BaseDirectoryNode,
    rs.content.BaseContentNode,
]:
    """
    SearchResult target can be an origin, snapshot, revision, release
    directory or a content
    """
    return NodeObjectFactory.create(f"search-result-{obj.targetType}", obj, info, **kw)


@query.field("contentByHash")
def content_by_hash_resolver(
    obj: None, info: GraphQLResolveInfo, **kw
) -> rs.content.ContentNode:
    return NodeObjectFactory.create("content-by-hash", obj, info, **kw)


# Connection resolvers
# A connection resolver should return an instance of BaseConnection


@query.field("origins")
def origins_resolver(
    obj: None, info: GraphQLResolveInfo, **kw
) -> rs.origin.OriginConnection:
    return ConnectionObjectFactory.create("origins", obj, info, **kw)


@origin.field("visits")
def visits_resolver(
    obj: rs.origin.BaseOriginNode, info: GraphQLResolveInfo, **kw
) -> rs.visit.OriginVisitConnection:
    return ConnectionObjectFactory.create("origin-visits", obj, info, **kw)


@origin.field("snapshots")
def origin_snapshots_resolver(
    obj: rs.origin.BaseOriginNode, info: GraphQLResolveInfo, **kw
) -> rs.snapshot.OriginSnapshotConnection:
    return ConnectionObjectFactory.create("origin-snapshots", obj, info, **kw)


@visit.field("statuses")
def visitstatus_resolver(
    obj: rs.visit.BaseVisitNode, info: GraphQLResolveInfo, **kw
) -> rs.visit_status.VisitStatusConnection:
    return ConnectionObjectFactory.create("visit-status", obj, info, **kw)


@snapshot.field("branches")
def snapshot_branches_resolver(
    obj: rs.snapshot.BaseSnapshotNode, info: GraphQLResolveInfo, **kw
) -> rs.snapshot_branch.SnapshotBranchConnection:
    return ConnectionObjectFactory.create("snapshot-branches", obj, info, **kw)


@revision.field("parents")
def revision_parents_resolver(
    obj: rs.revision.BaseRevisionNode, info: GraphQLResolveInfo, **kw
) -> rs.revision.ParentRevisionConnection:
    return ConnectionObjectFactory.create("revision-parents", obj, info, **kw)


@revision.field("revisionLog")
def revision_log_resolver(
    obj: rs.revision.BaseRevisionNode, info: GraphQLResolveInfo, **kw
) -> rs.revision.LogRevisionConnection:
    return ConnectionObjectFactory.create("revision-log", obj, info, **kw)


@directory.field("entries")
def directory_entries_resolver(
    obj: rs.directory.BaseDirectoryNode, info: GraphQLResolveInfo, **kw
) -> rs.directory_entry.DirectoryEntryConnection:
    return ConnectionObjectFactory.create("directory-entries", obj, info, **kw)


@query.field("resolveSwhid")
def search_swhid_resolver(
    obj: None, info: GraphQLResolveInfo, **kw
) -> rs.search.ResolveSwhidConnection:
    return ConnectionObjectFactory.create("resolve-swhid", obj, info, **kw)


@query.field("search")
def search_resolver(
    obj: None, info: GraphQLResolveInfo, **kw
) -> rs.search.SearchConnection:
    return ConnectionObjectFactory.create("search", obj, info, **kw)


# Other resolvers


@release_target.type_resolver
@directory_entry_target.type_resolver
@branch_target.type_resolver
@search_result_target.type_resolver
def union_resolver(
    obj: Union[
        rs.origin.BaseOriginNode,
        rs.revision.BaseRevisionNode,
        rs.release.BaseReleaseNode,
        rs.directory.BaseDirectoryNode,
        rs.content.BaseContentNode,
        rs.snapshot.BaseSnapshotNode,
        rs.snapshot_branch.BaseSnapshotBranchNode,
    ],
    *_,
) -> str:
    """
    Generic resolver for all the union types
    """
    return obj.is_type_of()


# BinaryString resolvers


@binary_string.field("text")
def binary_string_text_resolver(obj: bytes, *args, **kw) -> str:
    return obj.decode(utils.ENCODING, "replace")


@binary_string.field("base64")
def binary_string_base64_resolver(obj: bytes, *args, **kw) -> str:
    return utils.get_b64_string(obj)
