import graphene
from graphene import relay

from kaffepause.authentication.decorators import login_required
from kaffepause.breaks.mutations import (
    AcceptBreakInvitation,
    DeclineBreakInvitation,
    IgnoreBreakInvitation,
    InitiateBreak,
    RequestChange,
)
from kaffepause.breaks.selectors import (
    get_break,
    get_break_history,
    get_next_break,
    get_pending_break_invitations,
)
from kaffepause.breaks.types import (
    BreakConnection,
    BreakInvitationConnection,
    BreakInvitationsPresentationNode,
    BreakNode,
    BreaksPresentationNode,
)


class Query(graphene.ObjectType):
    breaks_presentation = graphene.Field(BreaksPresentationNode)
    break_invitations_presentation = graphene.Field(BreakInvitationsPresentationNode)
    next_break = graphene.Field(BreakNode)
    break_ = graphene.Field(BreakNode, uuid=graphene.UUID())
    pending_break_invitations = relay.ConnectionField(BreakInvitationConnection)
    break_history = relay.ConnectionField(BreakConnection)

    @login_required
    def resolve_breaks_presentation(self, info, **kwargs):
        return info.context["user"]

    @login_required
    def resolve_break_invitations_presentation(self, info, **kwargs):
        return info.context["user"]

    @login_required
    def resolve_next_break(self, info, **kwargs):
        current_user = info.context["user"]
        return get_next_break(actor=current_user)

    @login_required
    def resolve_break_(self, info, uuid, **kwargs):
        current_user = info.context["user"]
        return get_break(actor=current_user, uuid=uuid)

    @login_required
    def resolve_pending_break_invitations(self, info, **kwargs):
        current_user = info.context["user"]
        return get_pending_break_invitations(actor=current_user)

    @login_required
    def resolve_break_history(self, info, **kwargs):
        current_user = info.context["user"]
        return get_break_history(actor=current_user)


class Mutation(graphene.ObjectType):
    initiate_break = InitiateBreak.Field()
    accept_break_invitation = AcceptBreakInvitation.Field()
    decline_break_invitation = DeclineBreakInvitation.Field()
    ignore_break_invitation = IgnoreBreakInvitation.Field()
    request_change = RequestChange.Field()
