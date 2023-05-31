from kaffepause.authentication.jwt import (
    get_credentials,
    get_user_by_natural_key,
    get_user_by_token,
)
from kaffepause.authentication.selectors import (
    get_user_by_email,
    get_user_by_session_token,
    get_user_by_social_id,
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


class Neo4jSocialBackend:
    def authenticate(self, provider=None, access_token=None, **kwargs):
        if provider is None or access_token is None:
            return None

        if provider == "email":
            # Authenticate user using email provider
            user = get_user_by_email(access_token)
        else:
            # Authenticate user using social provider (e.g., Google, Facebook, etc.)
            user = get_user_by_social_id(provider, access_token)

        return user

    def get_user(self, user_id):
        return get_user_by_natural_key(user_id)


class Neo4jSessionBackend:
    def authenticate(self, session_token=None, **kwargs):
        if session_token is None:
            return None

        user = get_user_by_session_token(session_token)

        return user

    def get_user(self, user_id):
        return get_user_by_natural_key(user_id)
