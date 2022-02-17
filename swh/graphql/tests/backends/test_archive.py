from swh.graphql.backends import archive


def test_get_origin():
    assert archive.get_origin() == {"url": "example.com"}
