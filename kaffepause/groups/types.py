import graphene
from graphene import relay

import kaffepause.users.types


class GroupNode(graphene.ObjectType):
    class Meta:
        interfaces = (relay.Node,)
        name = "Group"

    uuid = graphene.UUID()
    name = graphene.String()
    created = graphene.DateTime()
    creator = graphene.Field(lambda: kaffepause.users.types.UserNode)
    members = graphene.List(lambda: kaffepause.users.types.UserNode)

    def resolve_creator(parent, info):
        return parent.creator.single()

    def resolve_members(parent, info):
        return parent.members.all()
