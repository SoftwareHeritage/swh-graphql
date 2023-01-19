# Copyright (C) 2022 The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information

from typing import Union

from swh.graphql.utils import utils
from swh.model.model import Revision
from swh.model.swhids import CoreSWHID, ObjectType

from .base_connection import BaseConnection, ConnectionData
from .base_node import BaseSWHNode
from .search import SearchResultNode
from .snapshot_branch import SnapshotBranchNode
from .target import TargetNode


class BaseRevisionNode(BaseSWHNode):
    """
    Base resolver for all the revision nodes
    """

    def _get_revision_by_id(self, revision_id):
        return self.archive.get_revisions([revision_id])[0]

    @property
    def parent_swhids(self):  # for ParentRevisionConnection resolver
        return [
            CoreSWHID(object_type=ObjectType.REVISION, object_id=parent_id)
            for parent_id in self._node.parents
        ]

    @property
    def directory_hash(self):  # for RevisionDirectoryNode resolver
        return self._node.directory

    @property
    def committerDate(self):  # To support the schema naming convention
        return self._node.committer_date

    @property
    def type(self):
        return self._node.type.value

    def is_type_of(self):
        # is_type_of is required only when resolving a UNION type
        # This is for ariadne to return the right type
        return "Revision"


class RevisionNode(BaseRevisionNode):
    """
    Node resolver for a revision requested directly with its SWHID
    """

    def _get_node_data(self):
        return self._get_revision_by_id(self.kwargs.get("swhid").object_id)


class TargetRevisionNode(BaseRevisionNode):
    """
    Node resolver for a revision requested as a target
    """

    _can_be_null = True
    obj: Union[
        SnapshotBranchNode,
        TargetNode,
        SearchResultNode,
    ]

    def _get_node_data(self):
        # self.obj.target_hash is the requested revision id
        if self.obj.target_hash:
            return self._get_revision_by_id(self.obj.target_hash)
        return None


class ParentRevisionConnection(BaseConnection):
    """
    Connection resolver for parent revisions in a revision
    """

    obj: BaseRevisionNode

    _node_class = BaseRevisionNode

    def _get_connection_data(self) -> ConnectionData:
        # self.obj is the current(child) revision
        # self.obj.parent_swhids is the list of parent SWHIDs

        # FIXME, using dummy(local) pagination, move pagination to backend
        # STORAGE-TODO (pagination)
        parents = self.archive.get_revisions(
            [x.object_id for x in self.obj.parent_swhids]
        )
        return utils.get_local_paginated_data(
            parents, self._get_first_arg(), self._get_after_arg()
        )


class LogRevisionConnection(BaseConnection):
    """
    Connection resolver for the log (list of revisions) in a revision
    """

    obj: BaseRevisionNode

    _node_class = BaseRevisionNode

    def _get_connection_data(self) -> ConnectionData:
        log = self.archive.get_revision_log([self.obj.swhid.object_id])
        # Storage is returning a list of dicts instead of model objects
        # Following loop is to reverse that operation
        # STORAGE-TODO; remove to_dict from storage.revision_log
        log = [Revision.from_dict(rev) for rev in log]
        # FIXME, using dummy(local) pagination, move pagination to backend
        # STORAGE-TODO (pagination)
        return utils.get_local_paginated_data(
            log, self._get_first_arg(), self._get_after_arg()
        )
