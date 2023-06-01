import graphene
from graphene import relay

from kaffepause.authentication.decorators import login_required
from kaffepause.notifications.mutations import MarkAllAsSeen
from kaffepause.notifications.selectors import get_notifications_for
from kaffepause.notifications.types import (
    NotificationBadgeCount,
    NotificationConnection,
)


class NotificationQuery(graphene.ObjectType):
    notifications = relay.ConnectionField(NotificationConnection)
    notification_badge_count = graphene.Field(NotificationBadgeCount)

    @login_required
    def resolve_notifications(self, info, **kwargs):
        # TODO: pagination
        return get_notifications_for(actor=info.context["user"])

    @login_required
    def resolve_notification_badge_count(self, info, **kwargs):
        return info.context["user"]


class Query(NotificationQuery, graphene.ObjectType):
    pass


class Mutation(graphene.ObjectType):
    mark_all_as_seen = MarkAllAsSeen.Field()
