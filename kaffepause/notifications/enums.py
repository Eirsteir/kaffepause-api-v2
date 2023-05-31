from enum import Enum

from kaffepause.common.bases import NeomodelRelationshipEnum


class SeenState(Enum):
    UNSEEN = "unseen"
    UNREAD = "unread"
    SEEN = "seen"
    SEEN_AND_READ = "seen and read"

    @classmethod
    def choices(cls):
        return {field: member.value for field, member in cls.__members__.items()}


class NotificationEntityType(Enum):
    USER_FRIEND_ADD = "User sends a friend request"
    USER_FRIEND_ACCEPT = "User accepts a friend request"
    BREAK_INVITATION_SENT_INDIVIDUALLY = "Individual break invitation is sent"
    BREAK_INVITATION_SENT_TO_GROUP = "Group break invitation is sent"
    BREAK_INVITATION_ACCEPTED = "Break invitation is accepted"
    BREAK_INVITATION_DECLINED = "Break invitation is declined"
    GROUP_MEMBER_ADDED = "User is added to group"
    GROUP_NAME_CHANGED = "A user changed name of a group"

    @classmethod
    def choices(cls):
        return {field: member.value for field, member in cls.__members__.items()}


class NotificationRelationship(NeomodelRelationshipEnum):
    NOTIFIES = "Notifies"
    ACTOR = "Is actor of"
    SUBJECT = "Is about"
