from typing import List
from uuid import UUID

from neomodel import db

from kaffepause.breaks.enums import BreakRelationship, InvitationReplyStatus
from kaffepause.breaks.exceptions import BreakNotFound
from kaffepause.breaks.models import Break, BreakInvitation
from kaffepause.common.utils import now
from kaffepause.groups.enums import GroupRelationship
from kaffepause.users.models import User


def can_user_edit_break(user: User, break_: Break) -> bool:
    return is_viewer_initiator(actor=user, break_=break_) and not break_.has_passed


def is_viewer_initiator(*, actor, break_: Break):
    return actor.is_initiator_of(break_)


def get_break_title(*, actor: User, break_: Break) -> str:
    if break_.has_passed:
        if actor.is_participant_of(break_=break_):
            return "Du tok en pause"
        elif actor.is_invited_to(break_=break_):
            return "%(sender_name)s inviterte deg til pause" % {
                "sender_name": break_.invitation_sender.short_name
            }

    if is_invited_and_has_not_replied(actor, break_):
        return "%(sender_name)s har invitert deg til pause" % {
            "sender_name": break_.invitation_sender.short_name
        }

    if is_initiator_and_has_invited(actor, break_):
        return "Du har invitert til pause"

    if is_initiator_and_has_planned_break(actor, break_):
        return "Du har planlagt en pause"

    return "Pause"


def is_initiator_and_has_planned_break(actor, break_):
    return actor.is_initiator_of(break_=break_) or actor.is_participant_of(
        break_=break_
    )


def is_initiator_and_has_invited(actor, break_):
    return actor.is_initiator_of(break_=break_) and break_.has_invitation


def is_invited_and_has_not_replied(actor, break_):
    return actor.is_invited_to(break_=break_) and not actor.is_participant_of(
        break_=break_
    )


def get_next_break(actor: User) -> Break:
    """Return the next break in time where actor is a participant."""
    return actor.breaks.filter(starting_at__gt=now()).first_or_none()


def get_break(actor: User, uuid: UUID) -> Break:
    """
    Return the break if actor has participated
    or has been invited (either individually or through group) or
    initiated to the requested break.
    """
    query = f"""
    MATCH
        (b:Break {{uuid: $break_uuid}}),
        (u:User {{uuid: $user_uuid}})
    WHERE (u)-[:{BreakRelationship.PARTICIPATED_IN}
                | :{BreakRelationship.INITIATED}]->(b)
        OR (u)-[:{BreakRelationship.SENT} | :{BreakRelationship.TO_USER}]
                -(:BreakInvitation)-[:{BreakRelationship.REGARDING}]->(b)
        OR (u)<-[:{GroupRelationship.HAS_MEMBER}]
                -(:Group)-[:{BreakRelationship.TO_GROUP}]
                -(:BreakInvitation)-[:{BreakRelationship.REGARDING}]->(b)
    RETURN b
    """
    params = dict(break_uuid=str(uuid), user_uuid=str(actor.uuid))
    results, meta = db.cypher_query(query, params, resolve_objects=True)

    if not results:
        raise BreakNotFound

    return results[0][0]


def get_all_break_invitations(actor: User) -> List[BreakInvitation]:
    query = f"""
        MATCH (user:User {{uuid: $user_uuid}})
        MATCH (user)<-[:{GroupRelationship.HAS_MEMBER}]-(group:Group)
        <-[:{BreakRelationship.TO_GROUP}]-(invitation:BreakInvitation)
        WITH invitation
        MATCH (invitation)-[:{BreakRelationship.REGARDING}]->(break:Break)
        RETURN invitation, break.starting_at
        ORDER BY break.starting_at DESC
        UNION
        MATCH (user:User {{uuid: $user_uuid}})
        MATCH (user)<-[:{BreakRelationship.TO_USER}]-(invitation:BreakInvitation)
        WITH invitation
        MATCH (invitation)-[:{BreakRelationship.REGARDING}]->(break:Break)
        RETURN invitation, break.starting_at
        ORDER BY break.starting_at DESC
    """
    params = dict(user_uuid=str(actor.uuid))
    results, meta = db.cypher_query(query, params=params)
    invitations = [BreakInvitation.inflate(row[0]) for row in results]
    return invitations


def get_pending_break_invitations(actor: User) -> List[BreakInvitation]:
    """Returns all non-expired unanswered break invitations."""
    query = (
        _get_unanswered_invitations_query()
        + f"""
    AND break_.starting_at > {_get_cypher_minutes_ago(5)}
    """
    )
    unanswered_invitations = _run_break_invitation_query(query, actor)
    return unanswered_invitations


def get_expired_break_invitations(actor: User) -> List[BreakInvitation]:
    query = (
        _get_unanswered_invitations_query()
        + f"""
    AND break_.starting_at < {_get_cypher_minutes_ago(5)}
    """
    )
    unanswered_invitations = _run_break_invitation_query(query, actor)
    return unanswered_invitations


def _get_unanswered_invitations_query() -> str:
    query = f"""
    MATCH (invitation:BreakInvitation)-[:{BreakRelationship.REGARDING}]->(break_:Break),
        (user:User {{uuid: $user_uuid}})
    WHERE NOT (user)-[:{BreakRelationship.ACCEPTED}
                        | {BreakRelationship.DECLINED}
                        | {BreakRelationship.IGNORED}]
                    ->(invitation)
        AND (
            (invitation)-[:{BreakRelationship.TO_USER}]->(user)
            OR (invitation)-[:{BreakRelationship.TO_GROUP}]
            ->(:Group)-[:{GroupRelationship.HAS_MEMBER}]->(user)
        )
    """
    return query


def _get_cypher_minutes_ago(minutes) -> str:
    return f"datetime().epochSeconds - (60*{minutes})"


def _run_break_invitation_query(query: str, actor: User) -> List[BreakInvitation]:
    query += "RETURN DISTINCT invitation"
    params = dict(user_uuid=str(actor.uuid))
    results, meta = db.cypher_query(query, params=params)
    breaks = [BreakInvitation.inflate(row[0]) for row in results]
    return breaks


def get_upcoming_breaks(actor: User) -> List[Break]:
    return actor.breaks.filter(starting_at__gt=now())


def get_break_history(actor: User) -> List[Break]:
    return actor.breaks.filter(starting_at__lt=now())


def get_invitation_context(actor: User, invitation: BreakInvitation):
    if not invitation:
        return None

    if actor.accepted_break_invitations.is_connected(invitation):
        return InvitationReplyStatus.ACCEPTED

    if actor.ignored_break_invitations.is_connected(invitation):
        return InvitationReplyStatus.IGNORED

    if actor.declined_break_invitations.is_connected(invitation):
        return InvitationReplyStatus.DECLINED

    if not invitation.is_expired:
        return InvitationReplyStatus.CAN_REPLY

    return InvitationReplyStatus.CANNOT_REPLY


# TODO: reuse enums
def get_invitation_addressees_annotated(invitation):
    if invitation is None:
        return []
    addressees = invitation.addressees.all()
    response_data = []
    for addressee in addressees:
        user_data = {"user": addressee}
        if invitation.confirmed.is_connected(addressee):
            user_data["rsvp"] = "ACCEPTED"
            user_data["rsvpTitle"] = "Godtatt"
        elif invitation.decliners.is_connected(addressee):
            user_data["rsvp"] = "DECLINED"
            user_data["rsvpTitle"] = "Avslått"
        elif invitation.non_attenders.is_connected(addressee):
            user_data["rsvp"] = "IGNORED"
            user_data["rsvpTitle"] = "Ikke svart"
        else:
            user_data["rsvp"] = "NOT_RESPONDED"
            user_data["rsvpTitle"] = "Ikke svart"
        response_data.append(user_data)
    return response_data
