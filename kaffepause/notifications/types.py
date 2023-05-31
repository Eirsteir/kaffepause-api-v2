import graphene
from graphene import relay

from kaffepause.notifications.enums import SeenState
from kaffepause.notifications.selectors import get_notification_badge_count
from kaffepause.users.types import UserNode


class NotificationNode(graphene.ObjectType):
    class Meta:
        interfaces = (relay.Node,)
        name = "Notification"

    uuid = graphene.UUID()
    seen_state = graphene.String()
    created = graphene.DateTime()
    entity_type = graphene.String()
    entity_id = graphene.String()
    text = graphene.String()
    kicker = graphene.String()
    url = graphene.String()
    actor = graphene.Field(UserNode)

    def resolve_seen_state(parent, info):
        return SeenState[parent.seen_state].name

    def resolve_actor(parent, info):
        return parent.actor.single()


class NotificationBadgeCount(graphene.ObjectType):
    class Meta:
        interfaces = (relay.Node,)
        name = "NotificationBadgeCount"

    count = graphene.Int()

    def resolve_count(parent, info):
        return get_notification_badge_count(actor=parent)


class NotificationConnection(relay.Connection):
    class Meta:
        node = NotificationNode
