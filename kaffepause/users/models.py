from neomodel import (
    DateTimeProperty,
    Relationship,
    RelationshipFrom,
    RelationshipTo,
    StringProperty,
    StructuredNode,
    UniqueIdProperty,
    ZeroOrMore,
    ZeroOrOne,
)

from kaffepause.authentication.enums import AccountRelationship
from kaffepause.authentication.models import BaseUser
from kaffepause.breaks.enums import BreakRelationship
from kaffepause.common.enums import (
    ACCOUNT,
    BREAK,
    BREAK_INVITATION,
    GROUP,
    LOCATION,
    NOTIFICATION,
    SESSION,
    USER,
)
from kaffepause.groups.enums import GroupRelationship
from kaffepause.location.enums import LocationRelationship
from kaffepause.notifications.enums import NotificationRelationship
from kaffepause.relationships.enums import UserRelationship
from kaffepause.relationships.models import FriendRel, RelationshipRel


class User(StructuredNode, BaseUser):
    uuid = UniqueIdProperty(db_property="id")  # Neomodel overrides field id
    name = StringProperty(required=True, index=True)
    email = StringProperty(unique_index=True, required=True)
    emailVerified = DateTimeProperty()
    image = StringProperty()

    account = RelationshipTo(ACCOUNT, AccountRelationship.HAS_ACCOUNT)
    sessions = RelationshipTo(SESSION, AccountRelationship.HAS_SESSION)

    friends = Relationship(USER, UserRelationship.ARE_FRIENDS, model=FriendRel)

    outgoing_friend_requests = RelationshipTo(
        USER, UserRelationship.REQUESTING_FRIENDSHIP, model=RelationshipRel
    )
    incoming_friend_requests = RelationshipFrom(
        USER, UserRelationship.REQUESTING_FRIENDSHIP, model=RelationshipRel
    )

    breaks = RelationshipTo(BREAK, BreakRelationship.PARTICIPATED_IN)
    initiated_breaks = RelationshipTo(BREAK, BreakRelationship.INITIATED)
    break_invitations = RelationshipFrom(BREAK_INVITATION, BreakRelationship.TO_USER)
    sent_break_invitations = RelationshipTo(BREAK_INVITATION, BreakRelationship.SENT)
    accepted_break_invitations = RelationshipTo(
        BREAK_INVITATION, BreakRelationship.ACCEPTED
    )
    declined_break_invitations = RelationshipTo(
        BREAK_INVITATION, BreakRelationship.DECLINED
    )
    ignored_break_invitations = RelationshipTo(
        BREAK_INVITATION, BreakRelationship.IGNORED
    )

    preferred_location = RelationshipTo(
        LOCATION, LocationRelationship.PREFERRED_LOCATION, cardinality=ZeroOrOne
    )
    current_location = RelationshipTo(
        LOCATION, LocationRelationship.CURRENT_LOCATION, cardinality=ZeroOrOne
    )
    custom_locations = RelationshipTo(
        LOCATION, LocationRelationship.USER_CREATED_LOCATION, cardinality=ZeroOrMore
    )

    notifications = RelationshipFrom(
        NOTIFICATION, NotificationRelationship.NOTIFIES, cardinality=ZeroOrMore
    )

    groups = RelationshipFrom(
        GROUP, GroupRelationship.HAS_MEMBER, cardinality=ZeroOrMore
    )

    class Meta:
        app_label = "users"

    @property
    def identity(self) -> str:
        return str(self.uuid)

    @classmethod
    def get_or_create(cls, object_, *props, **kwargs):
        return super().get_or_create({**object_.__dict__}, **kwargs)

    def send_friend_request(self, addressee):
        """Send a friend request to the given user."""
        return self.outgoing_friend_requests.connect(addressee)

    def cancel_friend_request(self, addressee):
        """Cancel a friend request sent to the given user."""
        return self.outgoing_friend_requests.disconnect(addressee)

    def reject_friend_request(self, requester):
        """Reject a friend request sent from the given user."""
        return self.incoming_friend_requests.disconnect(requester)

    def is_friends_with(self, user):
        return self.friends.is_connected(user)

    def has_send_friend_request_to(self, user):
        return self.outgoing_friend_requests.is_connected(user)

    def add_friend(self, other):
        """Disconnect requesting relationships and connect the users as friends."""
        self.outgoing_friend_requests.disconnect(other)
        self.following.connect(other)
        other.following.connect(self)
        return self.friends.connect(other)

    def remove_friend(self, friend):  # Returns None if not friends - ok?
        """Disconnect self and friend."""
        self.following.disconnect(friend)
        friend.following.disconnect(self)
        return self.friends.disconnect(friend)

    def can_perform_action_on_friend(self, friend):
        """
        A user can perform an arbitrary action on another
        if they are friends and the friend is not itself.
        """
        return self.friends.is_connected(friend) and friend is not self

    def get_current_status(self):
        return self.current_status.single()

    def get_preferred_location(self):
        return self.preferred_location.single()

    def get_current_location(self):
        return self.current_location.single()

    def is_initiator_of(self, break_):
        return self.initiated_breaks.is_connected(break_)

    def is_participant_of(self, break_):
        return self.breaks.is_connected(break_)

    def is_invited_to(self, break_):
        if break_.has_invitation:
            return self.break_invitations.is_connected(break_.get_invitation())
        return False

    def is_member_of(self, group):
        return self.groups.is_connected(group)

    @property
    def short_name(self):
        return self.name.split()[0]
