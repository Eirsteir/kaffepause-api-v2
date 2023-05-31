from kaffepause.common.exceptions import DefaultError


class RelationshipAlreadyExists(DefaultError):
    default_message = "Dette vennskapet finnes allerede"


class CannotAcceptFriendRequest(DefaultError):
    default_message = "Du kan ikke godta denne venneforespørselen"


class FriendRequestDoesNotExist(DefaultError):
    default_message = "Denne venneforespørselen finnes ikke"


class CannotRejectFriendRequest(DefaultError):
    default_message = "Du kan ikke avslå denne venneforespørselen"


class CannotUnfriendUser(DefaultError):
    default_message = (
        "Du kan ikke fjerne denne personen som venn siden dere ikke er venner"
    )
