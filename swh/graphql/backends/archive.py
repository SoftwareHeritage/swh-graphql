from swh.storage import get_storage


class Archive:
    def __init__(self):
        # FIXME, setup config
        self.storage = get_storage(
            cls="remote", url="http://moma.internal.softwareheritage.org:5002"
        )

    def get_origin(self, url):
        return self.storage.origin_get([url])[0]

    def get_origins(self, after=None, first=50):
        return self.storage.origin_list(page_token=after, limit=first)

    def search_origins(self, pattern, after=None, first=50):
        return self.storage.origin_search(
            url_pattern=pattern, page_token=after, limit=first
        )

    def get_origin_visits(self, origin_url, after=None, first=50):
        return self.storage.origin_visit_get(origin_url, page_token=after, limit=first)

    def get_origin_visit(self, origin_url, visit_id):
        return self.storage.origin_visit_get_by(origin_url, visit_id)

    def get_origin_latest_visit(self, origin_url):
        return self.storage.origin_visit_get_latest(origin_url)

    def get_visit_status(self, origin_url, visit_id, after=None, first=50):
        return self.storage.origin_visit_status_get(
            origin_url, visit_id, page_token=after, limit=first
        )

    def get_latest_visit_status(self, origin_url, visit_id):
        return self.storage.origin_visit_status_get_latest(origin_url, visit_id)

    def get_origin_snapshots(self, origin_url):
        return self.storage.origin_snapshot_get_all(origin_url)

    def get_snapshot_branches(self, snapshot, after, first, target_types, name_include):
        return self.storage.snapshot_get_branches(
            snapshot,
            branches_from=after,
            branches_count=first,
            target_types=target_types,
            branch_name_include_substring=name_include
        )

    def get_revisions(self, revision_ids):
        return self.storage.revision_get(revision_ids=revision_ids)

    def get_revision_log(self, revision_ids, after=None, first=50):
        return self.storage.revision_log(revisions=revision_ids, limit=first)

    def get_releases(self, release_ids):
        return self.storage.release_get(releases=release_ids)

    def get_directory_entries(self, directory_id):
        return self.storage.directory_ls(directory_id)

    def get_content(self, content_id):
        # FIXME, only for tests
        return self.storage.content_find({"sha1_git": content_id})
