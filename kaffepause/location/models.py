from neomodel import RelationshipFrom, StringProperty, StructuredNode

from kaffepause.common.enums import LOCATION
from kaffepause.common.properties import UUIDProperty
from kaffepause.location.enums import LocationRelationship


class Location(StructuredNode):
    uuid = UUIDProperty()
    title = StringProperty(required=True, index=True, max_length=100)
    type = StringProperty(required=False, max_length=30)
    item_type = StringProperty(required=False, index=True, max_length=30)
    children = RelationshipFrom(LOCATION, LocationRelationship.CHILD_OF)
