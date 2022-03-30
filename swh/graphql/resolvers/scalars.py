from ariadne import ScalarType

datetime_scalar = ScalarType("DateTime")
swhid_scalar = ScalarType("SWHId")
binary_text_scalar = ScalarType("BinaryText")


@datetime_scalar.serializer
def serialize_datetime(value):
    # FIXME, consider timezone, use core functions
    return value.timestamp()


@swhid_scalar.serializer
def serialize_swid(value):
    return value.hex()


@binary_text_scalar.serializer
def serialize_binary_text(value):
    # FIXME, consider non utf-8
    return value.decode("utf-8")
