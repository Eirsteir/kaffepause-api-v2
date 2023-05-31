import graphene


class AccountNode(graphene.ObjectType):
    class Meta:
        interfaces = (graphene.relay.Node,)
        name = "Account"

    uuid = graphene.UUID()
    type = graphene.String()
    provider = graphene.String()
