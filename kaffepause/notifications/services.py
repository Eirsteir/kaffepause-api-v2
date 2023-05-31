import logging
from datetime import datetime
from typing import List
from uuid import UUID

from kaffepause.notifications.enums import NotificationEntityType, SeenState
from kaffepause.notifications.messages import Messages
from kaffepause.notifications.models import Notification
from kaffepause.users.models import User

logger = logging.getLogger(__name__)


# TODO: signals: https://github.com/neo4j-contrib/django-neomodel#signals
def bulk_notify(
    *,
    notifiers: List[User],
    entity_type: NotificationEntityType,
    entity_id: UUID,
    actor: User,
    entity_potential_start_time: datetime = None,
    **message_kwargs,
) -> None:
    for notifier in notifiers:
        notify(
            user=notifier,
            entity_type=entity_type,
            entity_id=entity_id,
            actor=actor,
            entity_potential_start_time=entity_potential_start_time,
            **message_kwargs,
        )


def notify(
    *,
    user: User,
    entity_type: NotificationEntityType,
    entity_id: UUID,
    actor: User,
    entity_potential_start_time: datetime = None,
    **message_kwargs,
) -> None:
    # TODO: fail silently?
    text = Messages[entity_type](actor.name, **message_kwargs)
    notification = Notification(
        entity_type=entity_type.name,
        entity_id=entity_id,
        text=text,
        entity_potential_start_time=entity_potential_start_time,
    ).save()
    notification.notifier.connect(user)
    notification.actor.connect(actor)

    logger.debug(f"Notification created (notifier id: {user.uuid}): {notification}")


def mark_all_as_seen(*, user: User):
    # TODO: bulk_update?
    notifications_to_mark = user.notifications.filter(seen_state=SeenState.UNSEEN.name)
    for notification in notifications_to_mark:
        notification.seen_state = SeenState.SEEN.name
        notification.save()
