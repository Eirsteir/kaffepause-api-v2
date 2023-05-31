import graphene
from graphene import relay

from kaffepause.common.types import CountableConnection


class LocationNode(graphene.ObjectType):
    class Meta:
        interfaces = (relay.Node,)
        name = "Location"

    uuid = graphene.UUID()
    title = graphene.String()
    type = graphene.String()
    item_type = graphene.String()
    children = relay.ConnectionField(lambda: LocationConnection)

    def resolve_children(parent, info):
        return parent.children.all()


class LocationConnection(CountableConnection):
    class Meta:
        node = LocationNode
