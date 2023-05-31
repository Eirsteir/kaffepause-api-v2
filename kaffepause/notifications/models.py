from neomodel import (
    DateTimeProperty,
    One,
    RelationshipFrom,
    RelationshipTo,
    StringProperty,
)

from kaffepause.common.enums import USER
from kaffepause.common.models import TimeStampedNode
from kaffepause.common.properties import UUIDProperty
from kaffepause.notifications.enums import (
    NotificationEntityType,
    NotificationRelationship,
    SeenState,
)

#  https://docs.djangoproject.com/en/4.0/topics/i18n/translation/#:~:text=The%20strings%20you
from kaffepause.notifications.messages import (
    KickerMessages,
    entityTypeToEndpointMapping,
)


class Notification(TimeStampedNode):
    uuid = UUIDProperty()
    seen_state = StringProperty(
        choices=SeenState.choices(), default=SeenState.UNSEEN.name
    )
    entity_type = StringProperty(
        required=True, choices=NotificationEntityType.choices()
    )
    entity_id = StringProperty(required=True)
    entity_potential_start_time = DateTimeProperty(required=False)
    text = StringProperty(required=True, max_length=500)
    notifier = RelationshipTo(USER, NotificationRelationship.NOTIFIES, cardinality=One)
    actor = RelationshipFrom(USER, NotificationRelationship.ACTOR, cardinality=One)

    @property
    def url(self):
        entity_type = NotificationEntityType[self.entity_type]
        return entityTypeToEndpointMapping[entity_type].single(self.entity_id)

    @property
    def kicker(self):
        entity_type = NotificationEntityType[self.entity_type]
        return KickerMessages[entity_type](time=self.entity_potential_start_time)
