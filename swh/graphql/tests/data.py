# Copyright (C) 2022 The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information

# This module will be removed once the test data
# generation in SWH-wb moved to a shared location
# or to a new test data project

from datetime import timedelta

from swh.model.model import Origin, OriginVisit, OriginVisitStatus, Snapshot
from swh.storage.utils import now


def populate_dummy_data(storage):
    origins = get_origins()
    visits = get_visits(origins)
    snapshots = get_snapshots()
    status = get_visit_status(visits, snapshots)

    storage.origin_add(origins)
    storage.origin_visit_add(visits)
    storage.snapshot_add(snapshots)
    storage.origin_visit_status_add(status)


def get_origins():
    # Return two dummy origins
    return [
        Origin(url="http://example.com/forge1"),
        Origin(url="http://example.com/forge2"),
    ]


def get_visits(origins):
    # Return two visits each for an origin
    origin1, origin2 = origins
    return [
        OriginVisit(
            origin=origin1.url,
            date=now() - timedelta(minutes=200),
            type="git",
            visit=1,
        ),
        OriginVisit(
            origin=origin1.url,
            date=now(),
            type="git",
            visit=2,
        ),
        OriginVisit(
            origin=origin2.url,
            date=now() - timedelta(minutes=500),
            type="hg",
            visit=1,
        ),
        OriginVisit(
            origin=origin2.url,
            date=now(),
            type="hg",
            visit=2,
        ),
    ]


def get_visit_status(visits, snapshots):
    # Return one status per visit, adding only empty statpshots for now
    visit1, visit2, visit3, visit4 = visits
    (empty_snapshot,) = snapshots
    return [
        OriginVisitStatus(
            origin=visit1.origin,
            visit=visit1.visit,
            date=visit1.date,
            status="full",
            snapshot=empty_snapshot.id,
        ),
        OriginVisitStatus(
            origin=visit2.origin,
            visit=visit2.visit,
            date=visit1.date,
            status="full",
            snapshot=empty_snapshot.id,
        ),
        OriginVisitStatus(
            origin=visit3.origin,
            visit=visit3.visit,
            date=visit3.date,
            status="full",
            snapshot=empty_snapshot.id,
        ),
        OriginVisitStatus(
            origin=visit4.origin,
            visit=visit4.visit,
            date=visit4.date,
            status="full",
            snapshot=empty_snapshot.id,
        ),
    ]


def get_snapshots():
    empty_snapshot = Snapshot(branches={})
    return [empty_snapshot]
