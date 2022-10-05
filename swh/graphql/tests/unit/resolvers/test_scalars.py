# Copyright (C) 2022 The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information

import datetime

import pytest

from swh.graphql.errors import InvalidInputError
from swh.graphql.resolvers import scalars


def test_serialize_id():
    assert scalars.serialize_id("test") == "74657374"
    assert scalars.serialize_id(b"test") == "74657374"


def test_serialize_datetime():
    assert scalars.serialize_datetime("invalid") is None
    # python datetime
    date = datetime.datetime(2020, 5, 17)
    assert scalars.serialize_datetime(date) == date.isoformat()
    # FIXME, Timestamp with timezone


def test_validate_swhid_invalid():
    with pytest.raises(InvalidInputError):
        scalars.validate_swhid("invalid")


def test_validate_swhid():
    swhid = scalars.validate_swhid(f"swh:1:rev:{'1' * 40}")
    assert str(swhid) == "swh:1:rev:1111111111111111111111111111111111111111"


@pytest.mark.parametrize("content_hash", ["invalid", "test:invalid"])
def test_validate_content_hash_invalid_value(content_hash):
    with pytest.raises(InvalidInputError) as e:
        scalars.validate_content_hash(content_hash)
    assert "Invalid content checksum" in str(e.value)


def test_validate_content_hash_invalid_hash_algo():
    with pytest.raises(InvalidInputError) as e:
        scalars.validate_content_hash(f"invalid:{'1' * 40}")
    assert "Invalid hash algorithm" in str(e.value)


def test_validate_content_hash():
    assert (
        "sha1",
        b"\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11",
    ) == scalars.validate_content_hash(f"sha1:{'1' * 40}")
