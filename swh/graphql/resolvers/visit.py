# Copyright (C) 2022 The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information

from typing import Optional

from swh.graphql.utils import utils
from swh.model.model import OriginVisit

from .base_connection import BaseConnection, ConnectionData
from .base_node import BaseNode
from .origin import OriginNode


class BaseVisitNode(BaseNode):
    """
    Base resolver for all the visit nodes
    """

    _node: OriginVisit

    @property
    def id(self) -> str:
        # FIXME, use a better id
        return utils.get_b64_string(f"{self.origin}-{str(self.visit)}")

    @property
    def visitId(self) -> Optional[int]:  # To support the schema naming convention
        return self._node.visit


class OriginVisitNode(BaseVisitNode):
    """
    Node resolver for a visit requested directly with an origin URL
    and a visit ID
    """

    def _get_node_data(self) -> Optional[OriginVisit]:
        origin_url = self.kwargs.get("originUrl")
        visit_id = self.kwargs.get("visitId")
        return self.archive.get_origin_visit(origin_url=origin_url, visit_id=visit_id)  # type: ignore # noqa: B950


class LatestVisitNode(BaseVisitNode):
    """
    Node resolver for the latest visit in an origin
    """

    _can_be_null = True
    obj: OriginNode

    def _get_node_data(self):
        # self.obj.url is the origin URL
        return self.archive.get_origin_latest_visit(
            origin_url=self.obj.url,
            visit_type=self.kwargs.get("visitType"),
            allowed_statuses=self.kwargs.get("allowedStatuses"),
            require_snapshot=self.kwargs.get("requireSnapshot"),
        )


class OriginVisitConnection(BaseConnection):
    """
    Connection resolver for the visit objects in an origin
    """

    obj: OriginNode

    _node_class = BaseVisitNode

    def _get_connection_data(self) -> ConnectionData:
        # self.obj.url is the origin URL
        return ConnectionData(
            paged_result=self.archive.get_origin_visits(
                self.obj.url, after=self._get_after_arg(), first=self._get_first_arg()
            )
        )
