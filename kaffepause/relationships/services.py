from typing import Callable, Iterable

from kaffepause.notifications.enums import NotificationEntityType
from kaffepause.notifications.services import notify
from kaffepause.relationships.exceptions import (
    CannotAcceptFriendRequest,
    CannotRejectFriendRequest,
    CannotUnfriendUser,
    FriendRequestDoesNotExist,
    RelationshipAlreadyExists,
)
from kaffepause.relationships.models import FriendRel
from kaffepause.relationships.selectors import relationship_exists
from kaffepause.users.models import User


def send_friend_request(actor: User, to_user: User) -> FriendRel:
    """Connect two users with a requested friendship connection."""
    if relationship_exists(actor, to_user):
        raise RelationshipAlreadyExists

    request = actor.send_friend_request(to_user)
    notify(
        user=to_user,
        entity_type=NotificationEntityType.USER_FRIEND_ADD,
        entity_id=actor.uuid,
        actor=actor,
    )
    return request


def cancel_friend_request(actor: User, to_user: User):
    if actor.has_send_friend_request_to(to_user):
        return actor.cancel_friend_request(to_user)

    raise FriendRequestDoesNotExist


def accept_friend_request(actor: User, requester: User) -> FriendRel:
    """
    Create a friendship relationship between given nodes.
    The requester must first have sent a friend request.
    """

    existing_friendship = actor.friends.relationship(requester)
    if existing_friendship:
        return existing_friendship

    if can_reply_to_friend_request(actor, requester):
        friendship = requester.add_friend(actor)
        notify(
            user=requester,
            entity_type=NotificationEntityType.USER_FRIEND_ACCEPT,
            entity_id=actor.uuid,
            actor=actor,
        )
        return friendship

    raise CannotAcceptFriendRequest


def reject_friend_request(actor: User, requester: User) -> User:
    if can_reply_to_friend_request(actor, requester):
        return actor.reject_friend_request(requester)

    raise CannotRejectFriendRequest


def can_reply_to_friend_request(actor, requester) -> bool:
    """The actor can only reply to a friend request if the requester has sent one."""
    return actor.incoming_friend_requests.is_connected(requester)


def unfriend_user(actor: User, friend: User):
    return _perform_friend_action(
        action=actor.remove_friend, exc=CannotUnfriendUser(), users=(actor, friend)
    )


def _perform_friend_action(*, action: Callable, exc: Exception, users: Iterable[User]):
    actor, friend = users
    if actor.can_perform_action_on_friend(friend):
        return action(friend)

    raise exc
