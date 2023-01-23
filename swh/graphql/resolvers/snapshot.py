# Copyright (C) 2022 The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information

from typing import TYPE_CHECKING, Union

from swh.graphql.errors import NullableObjectError
from swh.graphql.utils import utils
from swh.model.model import Snapshot
from swh.model.swhids import ObjectType

from .base_connection import BaseConnection, ConnectionData
from .base_node import BaseSWHNode
from .origin import OriginNode
from .search import SearchResultNode
from .visit_status import BaseVisitStatusNode


class BaseSnapshotNode(BaseSWHNode):
    """
    Base resolver for all the snapshot nodes
    """

    def _get_snapshot_by_id(self, snapshot_id):
        # Return a Snapshot model object
        # branches is initialized as empty
        # Same pattern is used in directory
        return Snapshot(id=snapshot_id, branches={})

    def is_type_of(self):
        # is_type_of is required only when resolving a UNION type
        # This is for ariadne to return the right type
        return "Snapshot"


class SnapshotNode(BaseSnapshotNode):
    """
    Node resolver for a snapshot requested directly with its SWHID
    """

    def _get_node_data(self):
        """ """
        swhid = self.kwargs.get("swhid")
        if (
            swhid.object_type == ObjectType.SNAPSHOT
            and self.archive.is_object_available(swhid.object_id, swhid.object_type)
        ):
            return self._get_snapshot_by_id(swhid.object_id)
        return None


class VisitSnapshotNode(BaseSnapshotNode):
    """
    Node resolver for a snapshot requested from a visit-status
    """

    _can_be_null = True
    obj: BaseVisitStatusNode

    def _get_node_data(self):
        if self.obj.snapshotSWHID is None:
            raise NullableObjectError()
        snapshot_id = self.obj.snapshotSWHID.object_id
        return self._get_snapshot_by_id(snapshot_id)


class TargetSnapshotNode(BaseSnapshotNode):
    """
    Node resolver for a snapshot requested as a target
    """

    if TYPE_CHECKING:  # pragma: no cover
        from .target import BranchTargetNode

        obj: Union[SearchResultNode, BranchTargetNode]

    _can_be_null = True

    def _get_node_data(self):
        if self.obj.target_hash:
            return self._get_snapshot_by_id(self.obj.target_hash)
        return None


class OriginSnapshotConnection(BaseConnection):
    """
    Connection resolver for the snapshots in an origin
    """

    obj: OriginNode

    _node_class = BaseSnapshotNode

    def _get_connection_data(self) -> ConnectionData:
        results = self.archive.get_origin_snapshots(self.obj.url)
        snapshots = [Snapshot(id=snapshot, branches={}) for snapshot in results]
        # FIXME, using dummy(local) pagination, move pagination to backend
        # To remove localpagination, just drop the paginated call
        # STORAGE-TODO
        return utils.get_local_paginated_data(
            snapshots, self._get_first_arg(), self._get_after_arg()
        )
