from ariadne import ScalarType

from swh.model.fields.hashes import validate_sha1_git

# from swh.model.swhids import QualifiedSWHID

datetime_scalar = ScalarType("DateTime")
swhid_scalar = ScalarType("SWHID")
sha1_scalar = ScalarType("Sha1")
binary_text_scalar = ScalarType("BinaryText")
datetimezone_scalar = ScalarType("DateTimeZone")


@datetime_scalar.serializer
def serialize_datetime(value):
    # FIXME, consider timezone, use core functions
    return value.timestamp()


@sha1_scalar.serializer
def serialize_sha1(value):
    return value.hex()


@sha1_scalar.value_parser
def validate_sha1(value):
    # FIXME, handle the error and raise a Graphql one
    validate_sha1_git(value)
    return value


@binary_text_scalar.serializer
def serialize_binary_text(value):
    # FIXME
    return value.decode("utf-8")


@datetimezone_scalar.serializer
def serialize_datetimezone(value):
    return value.to_datetime().timestamp()
