from ariadne import load_schema_from_path, make_executable_schema, gql
from ariadne.asgi import GraphQL

from .resolvers import resolvers

type_defs = gql(load_schema_from_path("swh/graphql/schema/schema.graphql"))

schema = make_executable_schema(
    type_defs, resolvers.query, resolvers.origin, resolvers.origins, resolvers.visit
)

app = GraphQL(schema, debug=True)
