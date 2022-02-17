from ariadne import load_schema_from_path, make_executable_schema
from ariadne.asgi import GraphQL

from .resolvers import origin, query

type_defs = load_schema_from_path("swh/graphql/schema/schema.graphql")

schema = make_executable_schema(type_defs, query, origin.origin)

app = GraphQL(schema, debug=True)
