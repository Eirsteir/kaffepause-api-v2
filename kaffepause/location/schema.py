import graphene
from graphene import relay

from kaffepause.authentication.decorators import login_required
from kaffepause.location.mutations import AddUserLocation
from kaffepause.location.selectors import get_campus_locations
from kaffepause.location.types import LocationConnection


class LocationQuery(graphene.ObjectType):
    locations = relay.ConnectionField(LocationConnection, query=graphene.String())

    @login_required
    def resolve_locations(self, info, **kwargs):
        current_user = info.context.user
        return get_campus_locations(actor=current_user, **kwargs)


class LocationMutations(graphene.ObjectType):
    add_user_location = AddUserLocation.Field()


class Query(LocationQuery, graphene.ObjectType):
    pass


class Mutation(LocationMutations, graphene.ObjectType):
    pass
