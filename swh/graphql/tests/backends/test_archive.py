from swh.graphql.backends import archive


def test_get_origin():
    assert isinstance(archive.get_origins(), list)
