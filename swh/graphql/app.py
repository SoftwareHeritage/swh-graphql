from ariadne import gql, load_schema_from_path, make_executable_schema

from .resolvers import resolvers, scalars

type_defs = gql(load_schema_from_path("swh/graphql/schema/schema.graphql"))

schema = make_executable_schema(
    type_defs,
    resolvers.query,
    resolvers.origin,
    resolvers.visit,
    resolvers.visit_status,
    resolvers.snapshot,
    resolvers.snapshot_branch,
    resolvers.branch_target,
    scalars.datetime_scalar,
    scalars.swhid_scalar,
    scalars.binary_text_scalar,
    scalars.datetimezone_scalar,
)
