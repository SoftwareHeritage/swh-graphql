# Copyright (C) 2022 The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information

from typing import Union

from swh.graphql.errors import InvalidInputError
from swh.model import hashutil

from .base_node import BaseSWHNode
from .directory_entry import BaseDirectoryEntryNode
from .release import BaseReleaseNode
from .search import SearchResultNode
from .snapshot_branch import BaseSnapshotBranchNode


class BaseContentNode(BaseSWHNode):
    """
    Base resolver for all the content nodes
    """

    def _get_content_by_hashes(self, hashes: dict):
        content = self.archive.get_contents(hashes)
        # in case of a conflict, return the first element
        return content[0] if content else None

    @property
    def hashes(self):
        # FIXME, use a Node instead
        return {k: v.hex() for (k, v) in self._node.hashes().items()}

    @property
    def id(self):
        return self._node.sha1_git

    @property
    def data(self):
        # FIXME, return a Node object
        # FIXME, add more ways to retrieve data like binary string
        archive_url = "https://archive.softwareheritage.org/api/1/"
        content_sha1 = self._node.hashes()["sha1"]
        return {
            "url": f"{archive_url}content/sha1:{content_sha1.hex()}/raw/",
        }

    @property
    def mimeType(self):
        # FIXME, fetch data from the indexers
        return None

    @property
    def language(self):
        # FIXME, fetch data from the indexers
        return None

    @property
    def license(self):
        # FIXME, fetch data from the indexers
        return None

    def is_type_of(self):
        # is_type_of is required only when resolving a UNION type
        # This is for ariadne to return the right type
        return "Content"


class ContentNode(BaseContentNode):
    """
    Node resolver for a content requested directly with its SWHID
    """

    def _get_node_data(self):
        hashes = {"sha1_git": self.kwargs.get("swhid").object_id}
        return self._get_content_by_hashes(hashes)


class HashContentNode(BaseContentNode):
    """
    Node resolver for a content requested with one or more hashes
    """

    def _get_node_data(self):
        try:
            hashes = {
                hash_type: hashutil.hash_to_bytes(hash_value)
                for (hash_type, hash_value) in self.kwargs.items()
            }
        except ValueError as e:
            # raise an input error in case of an invalid hash
            raise InvalidInputError("Invalid content hash", e)
        if not hashes:
            raise InvalidInputError("At least one of the four hashes must be provided")
        return self._get_content_by_hashes(hashes)


class TargetContentNode(BaseContentNode):
    """
    Node resolver for a content requested as a target
    """

    _can_be_null = True
    obj: Union[
        SearchResultNode,
        BaseDirectoryEntryNode,
        BaseReleaseNode,
        BaseSnapshotBranchNode,
    ]

    def _get_node_data(self):
        return self._get_content_by_hashes(hashes={"sha1_git": self.obj.target_hash})
