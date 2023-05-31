from typing import List

from kaffepause.notifications.enums import SeenState
from kaffepause.notifications.models import Notification


def get_notifications_for(*, actor) -> List[Notification]:
    return actor.notifications.all()


def get_notification_badge_count(*, actor) -> int:
    return len(actor.notifications.filter(seen_state=SeenState.UNSEEN.name))
