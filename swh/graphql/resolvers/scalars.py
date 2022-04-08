from ariadne import ScalarType

datetime_scalar = ScalarType("DateTime")
swhid_scalar = ScalarType("SWHID")
sha1_scalar = ScalarType("Sha1")
binary_text_scalar = ScalarType("BinaryText")
datetimezone_scalar = ScalarType("DateTimeZone")


@datetime_scalar.serializer
def serialize_datetime(value):
    # FIXME, consider timezone, use core functions
    return value.timestamp()


@swhid_scalar.serializer
def serialize_swid(value):
    return value.hex()


@sha1_scalar.serializer
def serialize_sha1(value):
    return value.hex()


@binary_text_scalar.serializer
def serialize_binary_text(value):
    # FIXME
    return value.decode("utf-8")


@datetimezone_scalar.serializer
def serialize_datetimezone(value):
    return value.to_datetime().timestamp()
