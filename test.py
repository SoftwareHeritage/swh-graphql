from swh.storage import get_storage

storage = get_storage(cls="remote", url="http://moma.internal.softwareheritage.org:5002")
