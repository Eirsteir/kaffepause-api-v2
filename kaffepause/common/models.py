from datetime import datetime

import pytz
from neomodel import DateTimeProperty, StructuredNode, StructuredRel


class TimeStampedRel(StructuredRel):
    created = DateTimeProperty(default=lambda: datetime.now(pytz.utc))


class TimeStampedNode(StructuredNode):
    __abstract_node__ = True
    created = DateTimeProperty(default=lambda: datetime.now(pytz.utc))
