from kaffepause.common.bases import NeomodelRelationshipEnum


class AccountRelationship(NeomodelRelationshipEnum):
    HAS_ACCOUNT = "Has account"
    HAS_SESSION = "Has session"
