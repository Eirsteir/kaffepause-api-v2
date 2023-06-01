import graphene
from graphene import relay

from kaffepause.authentication.decorators import login_required
from kaffepause.users.mutations import ChangeProfilePicture, UpdatePreferredLocation
from kaffepause.users.selectors import get_user, get_users, search_users
from kaffepause.users.types import UserConnection, UserNode


class UserQuery(graphene.ObjectType):
    me = graphene.Field(UserNode)
    user = graphene.Field(UserNode, id=graphene.UUID())
    search_users = relay.ConnectionField(UserConnection, query=graphene.String())

    @login_required
    def resolve_me(self, info, **kwargs):
        return info.context["user"]

    @login_required
    def resolve_user(self, info, id):
        return get_user(uuid=id)

    @login_required
    def resolve_search_users(self, info, query=None, **kwargs):
        current_user = info.context["user"]
        if query:
            return search_users(query=query, searched_by=current_user)
        return get_users(fetched_by=current_user)


class ProfileMutation(graphene.ObjectType):
    change_profile_picture = ChangeProfilePicture.Field()
    update_preferred_location = UpdatePreferredLocation.Field()


class Query(UserQuery, graphene.ObjectType):
    pass


class Mutation(ProfileMutation, graphene.ObjectType):
    pass
