from kaffepause.common.enums import Endpoints
from kaffepause.common.utils import format_kicker_message
from kaffepause.notifications.enums import NotificationEntityType


def _get_user_friend_add_message(actor_name, **kwargs):
    return "%(actor_name)s har sendt deg en venneforespørsel." % {
        "actor_name": actor_name,
        **kwargs,
    }


def _get_user_friend_accept_message(actor_name, **kwargs):
    return "%(actor_name)s godtok venneforespørselen din." % {
        "actor_name": actor_name,
        **kwargs,
    }


def _get_break_invitation_sent_message(actor_name, **kwargs):
    if kwargs.get("location_name"):
        return (
            "%(actor_name)s vil ta en pause på %(location_name)s kl %(starting_at)s."
            % {"actor_name": actor_name, **kwargs}
        )
    return "%(actor_name)s vil ta en pause kl %(starting_at)s." % {
        "actor_name": actor_name,
        **kwargs,
    }


def _get_break_invitation_sent_to_group_message(actor_name, **kwargs):
    if kwargs.get("location_name"):
        return (
            "%(actor_name)s inviterte deg og %(group_name)s til en pause på %(location_name)s kl %(starting_at)s."
            % {"actor_name": actor_name, **kwargs}
        )
    return (
        "%(actor_name)s inviterte deg og %(group_name)s til en pause kl %(starting_at)s."
        % {"actor_name": actor_name, **kwargs}
    )


def _get_break_invitation_accepted_message(actor_name, **kwargs):
    return "%(actor_name)s godtok pauseinvitasjonen din." % {
        "actor_name": actor_name,
        **kwargs,
    }


def _get_break_invitation_declined_message(actor_name, **kwargs):
    return "%(actor_name)s avslo pauseinvitasjonen din." % {
        "actor_name": actor_name,
        **kwargs,
    }


def _get_group_member_added_message(actor_name, **kwargs):
    return "%(actor_name)s la deg til i gruppen %(group_name)s." % {
        "actor_name": actor_name,
        **kwargs,
    }


def _get_group_name_changed_message(actor_name, **kwargs):
    return (
        "%(actor_name)s ga nytt navn til gruppen %(group_name)s: %(new_group_name)s."
        % {"actor_name": actor_name, **kwargs}
    )


Messages = {
    NotificationEntityType.USER_FRIEND_ADD: _get_user_friend_add_message,
    NotificationEntityType.USER_FRIEND_ACCEPT: _get_user_friend_accept_message,
    NotificationEntityType.BREAK_INVITATION_SENT_INDIVIDUALLY: _get_break_invitation_sent_message,
    NotificationEntityType.BREAK_INVITATION_SENT_TO_GROUP: _get_break_invitation_sent_to_group_message,
    NotificationEntityType.BREAK_INVITATION_ACCEPTED: _get_break_invitation_accepted_message,
    NotificationEntityType.BREAK_INVITATION_DECLINED: _get_break_invitation_declined_message,
    NotificationEntityType.GROUP_MEMBER_ADDED: _get_group_member_added_message,
    NotificationEntityType.GROUP_NAME_CHANGED: _get_group_name_changed_message,
}


def _default_no_kicker_message(**kwargs):
    return None


def _get_break_invitation_sent_kicker_message(**kwargs):
    time = kwargs.get("time")
    if time:
        return format_kicker_message(time)
    return None


KickerMessages = {
    NotificationEntityType.USER_FRIEND_ADD: _default_no_kicker_message,
    NotificationEntityType.USER_FRIEND_ACCEPT: _default_no_kicker_message,
    NotificationEntityType.BREAK_INVITATION_SENT_INDIVIDUALLY: _get_break_invitation_sent_kicker_message,
    NotificationEntityType.BREAK_INVITATION_SENT_TO_GROUP: _get_break_invitation_sent_kicker_message,
    NotificationEntityType.BREAK_INVITATION_ACCEPTED: _default_no_kicker_message,
    NotificationEntityType.BREAK_INVITATION_DECLINED: _default_no_kicker_message,
    NotificationEntityType.GROUP_MEMBER_ADDED: _default_no_kicker_message,
    NotificationEntityType.GROUP_NAME_CHANGED: _default_no_kicker_message,
}
entityTypeToEndpointMapping = {
    NotificationEntityType.USER_FRIEND_ADD: Endpoints.USERS,
    NotificationEntityType.USER_FRIEND_ACCEPT: Endpoints.USERS,
    NotificationEntityType.BREAK_INVITATION_SENT_INDIVIDUALLY: Endpoints.BREAKS,
    NotificationEntityType.BREAK_INVITATION_SENT_TO_GROUP: Endpoints.BREAKS,
    NotificationEntityType.BREAK_INVITATION_DECLINED: Endpoints.BREAKS,
    NotificationEntityType.BREAK_INVITATION_ACCEPTED: Endpoints.BREAKS,
    NotificationEntityType.GROUP_MEMBER_ADDED: Endpoints.GROUPS,
    NotificationEntityType.GROUP_NAME_CHANGED: Endpoints.GROUPS,
}
