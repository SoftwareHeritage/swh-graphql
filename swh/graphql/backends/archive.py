from swh.storage import get_storage


class Archive:
    def __init__(self):
        self.storage = get_storage(
            cls="remote", url="http://moma.internal.softwareheritage.org:5002"
        )

    def get_origin(self, url):
        return self.storage.origin_get([url])[0]

    def get_origins(self, after=None, first=50):
        # change page_token to base64 encode
        return self.storage.origin_list(page_token=after, limit=first)

    def get_origin_visits(self, origin, after=None, first=50):
        return self.storage.origin_visit_get(origin, page_token=after, limit=first)
