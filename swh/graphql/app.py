from ariadne import gql, load_schema_from_path, make_executable_schema
from ariadne.asgi import GraphQL

from .resolvers import resolvers, scalars

type_defs = gql(load_schema_from_path("swh/graphql/schema/schema.graphql"))

schema = make_executable_schema(
    type_defs,
    resolvers.query,
    resolvers.origin,
    resolvers.origins,
    resolvers.visit,
    scalars.datetime_scalar,
    scalars.swhid_scalar,
)

app = GraphQL(schema, debug=True)
