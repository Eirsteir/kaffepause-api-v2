class JSONWebTokenError(Exception):
    default_message = None

    def __init__(self, message=None):
        if message is None:
            message = self.default_message

        super().__init__(message)


class PermissionDenied(JSONWebTokenError):
    default_message = "Du har ikke tilgang til å utføre denne handlingen"


class JSONWebTokenExpired(JSONWebTokenError):
    default_message = "Signature has expired"
