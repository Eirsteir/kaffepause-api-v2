from enum import Enum

from kaffepause.common.bases import NeomodelRelationshipEnum


class LocationRelationship(NeomodelRelationshipEnum):
    CHILD_OF = "CHILD_OF"
    PREFERRED_LOCATION = "PREFERRED_LOCATION"
    CURRENT_LOCATION = "CURRENT_LOCATION"
    USER_CREATED_LOCATION = "USER_CREATED_LOCATION"


class LocationType(Enum):
    UNIVERSITY = "university"
    HOSPITAL = "hospital"


class LocationItemType(Enum):
    CAMPUS = "campus"
    GROUP = "group"
