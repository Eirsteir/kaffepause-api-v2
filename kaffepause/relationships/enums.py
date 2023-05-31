from kaffepause.common.bases import NeomodelRelationshipEnum


class UserRelationship(NeomodelRelationshipEnum):
    ARE_FRIENDS = "Are friends"
    REQUESTING_FRIENDSHIP = "Requested"


class NonRelatedRelationship(NeomodelRelationshipEnum):
    CAN_REQUEST = "Can request"
    CANNOT_REQUEST = "Cannot request"
    OUTGOING_REQUEST = "Outgoing request"
    INCOMING_REQUEST = "Incoming request"
