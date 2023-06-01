import graphene

from kaffepause.breaks.models import BreakInvitation
from kaffepause.breaks.services import (
    accept_break_invitation,
    create_break_and_invitation,
    decline_break_invitation,
    ignore_break_invitation,
    request_change,
)
from kaffepause.breaks.types import BreakInvitationNode, BreakNode
from kaffepause.common.bases import LoginRequiredMixin, Output


class InitiateBreak(LoginRequiredMixin, Output, graphene.Mutation):
    class Arguments:
        addressees = graphene.List(graphene.UUID, required=False)
        recipient_group_id = graphene.UUID(required=False)
        start_time = graphene.DateTime(required=True)
        location = graphene.UUID(required=False)

    break_ = graphene.Field(BreakNode)

    @classmethod
    def resolve_mutation(
        cls,
        root,
        info,
        addressees=None,
        recipient_group_id=None,
        start_time=None,
        location=None,
    ):
        current_user = info.context["user"]
        break_ = create_break_and_invitation(
            actor=current_user,
            recipient_user_ids=addressees,
            recipient_group_id=recipient_group_id,
            starting_at=start_time,
            location=location,
        )
        return cls(break_=break_, success=True)


class BreakInvitationAction(LoginRequiredMixin, Output, graphene.Mutation):
    class Arguments:
        invitation = graphene.UUID()

    _invitation_action = None

    invitation = graphene.Field(BreakInvitationNode)

    @classmethod
    def resolve_mutation(cls, root, info, invitation):
        invitation = BreakInvitation.nodes.get(uuid=invitation)
        current_user = info.context["user"]
        invitation = cls._invitation_action(actor=current_user, invitation=invitation)
        return cls(invitation=invitation, success=True)


class AcceptBreakInvitation(BreakInvitationAction):
    _invitation_action = accept_break_invitation


class DeclineBreakInvitation(BreakInvitationAction):
    _invitation_action = decline_break_invitation


class IgnoreBreakInvitation(BreakInvitationAction):
    _invitation_action = ignore_break_invitation


class RequestChange(LoginRequiredMixin, Output, graphene.Mutation):
    class Arguments:
        break_uuid = graphene.UUID(required=True)
        requested_time = graphene.DateTime(required=False)
        requested_location_uuid = graphene.UUID(required=False)

    break_ = graphene.Field(BreakNode)

    @classmethod
    def resolve_mutation(
        cls, root, info, break_uuid, requested_time=None, requested_location_uuid=None
    ):
        current_user = info.context["user"]

        break_ = request_change(
            actor=current_user,
            break_uuid=break_uuid,
            requested_time=requested_time,
            requested_location_uuid=requested_location_uuid,
        )
        return cls(break_=break_, success=True)
