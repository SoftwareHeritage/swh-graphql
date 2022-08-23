# Copyright (C) 2022 The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information

from collections import namedtuple

from swh.graphql.backends import archive
from swh.graphql.errors import ObjectNotFoundError
from swh.graphql.utils import utils
from swh.storage.interface import PagedResult

from .base_connection import BaseConnection
from .base_node import BaseNode


class BaseSnapshotBranchNode(BaseNode):

    # target field for this node is a UNION type
    # It is resolved in the top level (resolvers.resolvers.py)

    def _get_node_from_data(self, node_data: tuple):
        # node_data is a tuple as returned by _get_paged_result in
        # SnapshotBranchConnection and _get_node_data in AliasSnapshotBranchNode
        # overriding to support this special data structure
        branch_name, branch_obj = node_data
        node = {
            "name": branch_name,
            "type": branch_obj.target_type.value,
            "target_hash": branch_obj.target,
        }
        return namedtuple("NodeObj", node.keys())(*node.values())

    def is_type_of(self):
        return "Branch"

    def snapshot_swhid(self):
        raise NotImplementedError("Implement snapshot_swhid")


class ConnectionSnapshotBranchNode(BaseSnapshotBranchNode):
    """
    Node resolver for a snapshot branch requested from a snapshot branch connection
    """

    # obj: SnapshotBranchConnection

    def snapshot_swhid(self):
        # self.obj is SnapshotBranchConnection.
        # hence self.obj.obj is always of type BaseSnapshotNode

        # This will fail when this node is used for a connection that directly
        # requests snapshot branches with a snapshot SWHID. Create a new node object
        # in that case
        return self.obj.obj.swhid


class AliasSnapshotBranchNode(BaseSnapshotBranchNode):

    obj: ConnectionSnapshotBranchNode

    def _get_node_data(self):
        # snapshot_swhid will be provided by the parent object (self.obj)
        # As of now ConnectionSnapshotBranchNode is the only possible parent
        # implement snapshot_swhid in each of them if you are planning to add more parents.
        # eg for another possible parent: A node class that can get a snapshot branch directly
        # using snapshot id and branch name, snapshot_swhid will be available in the
        # user input (kwargs) in that case

        snapshot_swhid = self.obj.snapshot_swhid()
        target_branch = self.obj.target_hash

        alias_branch = archive.Archive().get_snapshot_branches(
            snapshot_swhid.object_id, first=1, name_include=target_branch
        )
        if target_branch not in alias_branch["branches"]:
            raise ObjectNotFoundError(
                f"Branch name with {target_branch.decode()} is not available"
            )
        # this will be serialized in _get_node_from_data method in the base class
        return (target_branch, alias_branch["branches"][target_branch])


class SnapshotBranchConnection(BaseConnection):
    """
    Connection resolver for the branches in a snapshot
    """

    from .snapshot import BaseSnapshotNode

    obj: BaseSnapshotNode

    _node_class = ConnectionSnapshotBranchNode

    def _get_paged_result(self) -> PagedResult:
        result = archive.Archive().get_snapshot_branches(
            self.obj.swhid.object_id,
            after=self._get_after_arg(),
            first=self._get_first_arg(),
            target_types=self.kwargs.get("types"),
            name_include=self._get_name_include_arg(),
        )
        # endCursor is the last branch name, logic for that
        end_cusrsor = (
            result["next_branch"] if result["next_branch"] is not None else None
        )
        # FIXME, this pagination is not consistent with other connections
        # FIX in swh-storage to return PagedResult
        # STORAGE-TODO

        # this will be serialized in _get_node_from_data method in the node class
        return PagedResult(
            results=result["branches"].items(), next_page_token=end_cusrsor
        )

    def _get_after_arg(self):
        # after argument must be an empty string by default
        after = super()._get_after_arg()
        return after.encode() if after else b""

    def _get_name_include_arg(self):
        name_include = self.kwargs.get("nameInclude", None)
        return name_include.encode() if name_include else None

    def _get_index_cursor(self, index: int, node: ConnectionSnapshotBranchNode):
        # Snapshot branch is using a different cursor, hence the override
        return utils.get_encoded_cursor(node.name)
