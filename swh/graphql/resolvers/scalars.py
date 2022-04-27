from ariadne import ScalarType

from swh.graphql.utils import utils
from swh.model.fields.hashes import validate_sha1_git
from swh.model.model import TimestampWithTimezone
from swh.model.swhids import QualifiedSWHID

datetime_scalar = ScalarType("DateTime")
swhid_scalar = ScalarType("SWHID")
sha1_scalar = ScalarType("Sha1")
binary_text_scalar = ScalarType("BinaryText")


@sha1_scalar.serializer
def serialize_sha1(value):
    return value.hex()


@sha1_scalar.value_parser
def validate_and_get_sha1_git(value):
    # FIXME, handle the error and raise a Graphql one
    validate_sha1_git(value)
    return bytearray.fromhex(value)


@binary_text_scalar.serializer
def serialize_binary_text(value):
    return value.decode("utf-8")


@datetime_scalar.serializer
def serialize_datetime(value):
    # FIXME, handle error and return None
    if type(value) == TimestampWithTimezone:
        value = value.to_datetime()
    return utils.get_formatted_date(value)


@swhid_scalar.value_parser
def validate_swhid(value):
    return QualifiedSWHID.from_string(value)
