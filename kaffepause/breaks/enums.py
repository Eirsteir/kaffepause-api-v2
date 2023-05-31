from enum import Enum

from kaffepause.common.bases import NeomodelRelationshipEnum


class InvitationReplyStatus(Enum):
    CAN_REPLY = "can reply"
    CANNOT_REPLY = "cannot reply"
    ACCEPTED = "accepted"
    DECLINED = "has declined"
    IGNORED = "has ignored"


class BreakRelationship(NeomodelRelationshipEnum):
    PARTICIPATED_IN = "Participated in"
    INITIATED = "Initiated"
    SENT = "Sent"
    TO_USER = "To user"
    TO_GROUP = "To group"
    REGARDING = "Regarding"
    ACCEPTED = "Accepted"
    DECLINED = "Declined"
    IGNORED = "Ignored"
    LOCATED_AT = "Located at"
    REQUESTED_CHANGE = "Requested change"
    CHANGE_REQUESTED_FOR = "Change request for"
    ACCEPTED_CHANGE = "Accepted change"
    DENIED_CHANGE = "Denied change"
    REQUESTED_LOCATION = "Requested location"
