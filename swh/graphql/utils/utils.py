import base64


def encode(text):
    return base64.b64encode(bytes(text, "utf-8")).decode("utf-8")


def get_encoded_cursor(cursor):
    if cursor is None:
        return None
    return base64.b64encode(bytes(cursor, "utf-8")).decode("utf-8")


def get_decoded_cursor(cursor):
    if cursor is None:
        return None
    return base64.b64decode(cursor).decode("utf-8")


def str_to_swid(str_swid):
    return bytearray.fromhex(str_swid)
