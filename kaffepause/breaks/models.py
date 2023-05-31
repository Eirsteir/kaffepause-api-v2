from datetime import datetime

from neomodel import (
    DateTimeProperty,
    One,
    RelationshipFrom,
    RelationshipTo,
    StructuredNode,
    ZeroOrMore,
    ZeroOrOne,
)

from kaffepause.breaks.enums import BreakRelationship
from kaffepause.breaks.exceptions import (
    AlreadyReplied,
    InvalidBreakStartTime,
    InvitationExpired,
    InvitationNotAddressedAtUser,
)
from kaffepause.common.enums import (
    BREAK,
    BREAK_INVITATION,
    CHANGE_REQUEST,
    GROUP,
    LOCATION,
    USER,
)
from kaffepause.common.models import TimeStampedNode, TimeStampedRel
from kaffepause.common.properties import UUIDProperty
from kaffepause.common.utils import (
    fifteen_minutes_from_now,
    format_kicker_message,
    time_from_now,
)


class Break(StructuredNode):
    uuid = UUIDProperty()
    starting_at = DateTimeProperty(default=lambda: fifteen_minutes_from_now())
    participants = RelationshipFrom(USER, BreakRelationship.PARTICIPATED_IN)
    initiator = RelationshipFrom(USER, BreakRelationship.INITIATED)
    invitation = RelationshipFrom(BREAK_INVITATION, BreakRelationship.REGARDING)
    location = RelationshipTo(
        LOCATION, BreakRelationship.LOCATED_AT, cardinality=ZeroOrOne
    )
    change_requests = RelationshipFrom(
        CHANGE_REQUEST, BreakRelationship.CHANGE_REQUESTED_FOR, cardinality=ZeroOrMore
    )

    @classmethod
    def create(cls, *props, **kwargs):
        cls.clean(*props, **kwargs)
        return super().create(*props, **kwargs)

    def clean(self, *props, **kwargs):
        start_time = self.get("starting_at")
        if datetime.utcnow() >= start_time or not start_time:
            raise InvalidBreakStartTime
        elif time_from_now(minutes=5) >= start_time:
            raise InvalidBreakStartTime("Pausen må begynne om minimum 5 minutter.")

    @property
    def is_expired(self):
        return time_from_now(minutes=5) >= self.starting_at

    @property
    def has_passed(self):
        return datetime.utcnow() >= self.starting_at

    @property
    def kicker(self):
        if self.starting_at > datetime.utcnow():
            return format_kicker_message(self.starting_at)
        return "Utgått"

    @property
    def has_invitation(self):
        return self.invitation.single() is not None

    @property
    def invitation_sender(self):
        return self.get_invitation().get_sender()

    def get_invitation(self):
        return self.invitation.single()

    def get_participants(self):
        return self.participants.all()

    def get_location(self):
        return self.location.single()


class BreakInvitation(StructuredNode):
    uuid = UUIDProperty()
    created = DateTimeProperty(default=lambda: datetime.utcnow())
    sender = RelationshipFrom(USER, BreakRelationship.SENT, cardinality=One)
    addressees = RelationshipTo(USER, BreakRelationship.TO_USER, cardinality=ZeroOrMore)
    recipient_group = RelationshipTo(
        GROUP, BreakRelationship.TO_GROUP, cardinality=ZeroOrOne
    )
    subject = RelationshipTo(BREAK, BreakRelationship.REGARDING, cardinality=One)

    confirmed = RelationshipFrom(USER, BreakRelationship.ACCEPTED, model=TimeStampedRel)
    decliners = RelationshipFrom(USER, BreakRelationship.DECLINED, model=TimeStampedRel)
    non_attenders = RelationshipFrom(
        USER, BreakRelationship.IGNORED, model=TimeStampedRel
    )

    @property
    def is_expired(self):
        return self.get_subject().is_expired

    @property
    def has_addressees(self):
        return bool(self.addressees)

    def get_sender(self):
        return self.sender.single()

    def get_subject(self):
        return self.subject.single()

    def get_addressee_count(self):
        return len(self.addressees.all())

    def accept_on_behalf_of(self, user):
        self.confirmed.connect(user)

    def decline_on_behalf_of(self, user):
        self.decliners.connect(user)

    def ignore_on_behalf_of(self, user):
        self.non_attenders.connect(user)

    def ready_for_reply(self, user):
        self._check_expiry()
        self._assert_is_addressed_at_user(user)
        self._assert_user_have_not_replied(user)

    def _check_expiry(self):
        if self.is_expired:
            raise InvitationExpired

    def _assert_is_addressed_at_user(self, user):
        if not self.addressees.is_connected(user) and not user.is_member_of(
            self.recipient_group.single()
        ):
            raise InvitationNotAddressedAtUser

    def _assert_user_have_not_replied(self, user):
        has_replied = user in self.confirmed or user in self.decliners

        if has_replied:
            raise AlreadyReplied


class ChangeRequest(TimeStampedNode):
    uuid = UUIDProperty()
    requested_time = DateTimeProperty()
    requested_location = RelationshipTo(
        LOCATION, BreakRelationship.REQUESTED_LOCATION, cardinality=ZeroOrOne
    )

    requested_by = RelationshipFrom(
        USER, BreakRelationship.REQUESTED_CHANGE, cardinality=One
    )
    requested_for = RelationshipTo(
        BREAK, BreakRelationship.CHANGE_REQUESTED_FOR, cardinality=One
    )
    accepted = RelationshipTo(
        BREAK, BreakRelationship.ACCEPTED_CHANGE, cardinality=ZeroOrOne
    )
    denied = RelationshipTo(
        BREAK, BreakRelationship.DENIED_CHANGE, cardinality=ZeroOrOne
    )
