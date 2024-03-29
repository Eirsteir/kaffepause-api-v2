from kaffepause.authentication.jwt import (
    get_credentials,
    get_user_by_natural_key,
    get_user_by_token,
)


class JSONWebTokenBackend:
    def authenticate(self, request=None, **kwargs):
        if request is None:
            return None

        token = get_credentials(request, **kwargs)

        if token is not None:
            return get_user_by_token(token, request)

        return None

    def get_user(self, user_id):
        return get_user_by_natural_key(user_id)
