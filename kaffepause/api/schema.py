import graphene

import kaffepause.accounts.schema
import kaffepause.authentication.schema
import kaffepause.breaks.schema
import kaffepause.groups.schema
import kaffepause.location.schema
import kaffepause.notifications.schema
import kaffepause.relationships.schema
import kaffepause.users.schema


class Query(
    kaffepause.accounts.schema.Query,
    kaffepause.users.schema.Query,
    kaffepause.relationships.schema.Query,
    kaffepause.breaks.schema.Query,
    kaffepause.location.schema.Query,
    kaffepause.notifications.schema.Query,
    kaffepause.groups.schema.Query,
    graphene.ObjectType,
):
    pass


class Mutation(
    kaffepause.authentication.schema.Mutation,
    kaffepause.users.schema.Mutation,
    kaffepause.relationships.schema.Mutation,
    kaffepause.breaks.schema.Mutation,
    kaffepause.location.schema.Mutation,
    kaffepause.notifications.schema.Mutation,
    kaffepause.groups.schema.Mutation,
    graphene.ObjectType,
):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
