import graphene

from kaffepause.common.bases import LoginRequiredMixin, Output
from kaffepause.notifications.services import mark_all_as_seen
from kaffepause.notifications.types import NotificationBadgeCount


class MarkAllAsSeen(LoginRequiredMixin, Output, graphene.Mutation):
    notification_badge_count = graphene.Field(NotificationBadgeCount)

    @classmethod
    def resolve_mutation(cls, root, info):
        current_user = info.context.user
        mark_all_as_seen(user=current_user)
        return cls(notification_badge_count=current_user, success=True)
