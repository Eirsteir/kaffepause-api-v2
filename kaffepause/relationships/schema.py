import graphene
from graphene import relay

from kaffepause.authentication.decorators import login_required
from kaffepause.relationships.mutations import (
    AcceptFriendRequest,
    CancelFriendRequest,
    RejectFriendRequest,
    SendFriendRequest,
    UnfriendUser,
)
from kaffepause.relationships.selectors import (
    get_friend_recommendations,
    get_incoming_requests,
    get_outgoing_requests,
)
from kaffepause.users.types import UserConnection


class Query(graphene.ObjectType):
    friending_possibilities = relay.ConnectionField(UserConnection)
    outgoing_friend_requests = relay.ConnectionField(UserConnection)
    friend_recommendations = relay.ConnectionField(UserConnection)

    @login_required
    def resolve_friending_possibilities(self, info, **kwargs):
        user = info.context["user"]
        return get_incoming_requests(user)

    @login_required
    def resolve_outgoing_friend_requests(self, info, **kwargs):
        user = info.context["user"]
        return get_outgoing_requests(user)

    @login_required
    def resolve_friend_recommendations(self, info, **kwargs):
        user = info.context["user"]
        return get_friend_recommendations(user, limit=10)


class Mutation(graphene.ObjectType):
    send_friend_request = SendFriendRequest.Field()
    cancel_friend_request = CancelFriendRequest.Field()
    accept_friend_request = AcceptFriendRequest.Field()
    reject_friend_request = RejectFriendRequest.Field()
    unfriend_user = UnfriendUser.Field()
