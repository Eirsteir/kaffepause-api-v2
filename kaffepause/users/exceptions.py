from kaffepause.common.exceptions import DefaultError


class UserDoesNotExist(DefaultError):
    default_message = "Denne brukeren finnes ikke"
