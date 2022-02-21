from ariadne import load_schema_from_path, make_executable_schema, gql
from ariadne.asgi import GraphQL

from .resolvers import origin, query

type_defs = gql(load_schema_from_path("swh/graphql/schema/schema.graphql"))

schema = make_executable_schema(type_defs, query, origin.origin, origin.origins)

app = GraphQL(schema, debug=True)
