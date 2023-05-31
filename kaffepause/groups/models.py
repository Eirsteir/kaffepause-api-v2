from neomodel import One, OneOrMore, RelationshipFrom, RelationshipTo, StringProperty

from kaffepause.common.enums import USER
from kaffepause.common.models import TimeStampedNode
from kaffepause.common.properties import UUIDProperty
from kaffepause.groups.enums import GroupRelationship


class Group(TimeStampedNode):
    uuid = UUIDProperty()
    name = StringProperty(required=True)
    members = RelationshipTo(USER, GroupRelationship.HAS_MEMBER, cardinality=OneOrMore)
    creator = RelationshipFrom(USER, GroupRelationship.CREATED_GROUP, cardinality=One)
