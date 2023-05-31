from datetime import datetime

import pytz
from neomodel import DateTimeProperty, FloatProperty, StructuredRel


class RelationshipRel(StructuredRel):
    since = DateTimeProperty(default=lambda: datetime.now(pytz.utc))


class FriendRel(RelationshipRel):
    weight = FloatProperty(default=1.0)
