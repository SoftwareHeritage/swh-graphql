from ariadne import ScalarType

datetime_scalar = ScalarType("DateTime")
swhid_scalar = ScalarType("SWHId")


@datetime_scalar.serializer
def serialize_datetime(value):
    return value.timestamp()


@swhid_scalar.serializer
def serialize_swid(value):
    return value.hex()
