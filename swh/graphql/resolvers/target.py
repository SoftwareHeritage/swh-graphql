# Copyright (C) 2022-2023 The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information

from typing import TYPE_CHECKING, Dict, Optional, Union

from swh.model.model import CoreSWHID, Sha1Git
from swh.model.swhids import ObjectType as SwhidObjectType

from .base_node import BaseNode


class TargetNode(BaseNode):
    """
    Intermediate node between an object and its target
    Created for schema clarity and to handle missing target
    nodes in the archive
    """

    # 'node' field in this object is resolved in the top level

    if TYPE_CHECKING:  # pragma: no cover
        from .directory_entry import BaseDirectoryEntryNode
        from .release import BaseReleaseNode

        obj: Union[BaseReleaseNode, BaseDirectoryEntryNode]

    @property
    def type(self) -> str:
        # field exposed in the schema
        return self.obj.target_type().value

    @property
    def swhid(self) -> Optional[CoreSWHID]:
        # field exposed in the schema
        # use the target type and hash to construct the SWHID
        mapping = {  # to map models.ObjectId to swhids.ObjectId
            "revision": SwhidObjectType.REVISION,
            "release": SwhidObjectType.RELEASE,
            "directory": SwhidObjectType.DIRECTORY,
            "content": SwhidObjectType.CONTENT,
        }
        if self.target_hash:
            return CoreSWHID(object_type=mapping[self.type], object_id=self.target_hash)
        return None

    @property
    def target_hash(self) -> Optional[Sha1Git]:
        # field NOT exposed in the schema
        # to be used while retrieving the node object
        # This will always be the target_hash from the parent (slef.obj)
        return self.obj.target_hash()

    def _get_node_data(self) -> Dict:
        # No exta data to fetch; everything is available from self.obj
        return {}
