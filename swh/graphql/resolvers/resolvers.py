from ariadne import ObjectType


def resolver_node_factory(resolver_type):
    mapping = {"origin": "", "visit": ""}
    return mapping[resolver_type]()


def resolver_list_factory(resolver_type):
    mapping = {
        "origins": "",
        "visits": "",
    }
    return mapping[resolver_type]()


query = ObjectType("Query")

# Nodes


@query.origin
def origin():
    return resolver_node_factory("origin",)


# Connections


@query.origins
def origins():
    return resolver_list_factory("origin",)


# @origin.visits
# def visits():
#     pass


# Other
