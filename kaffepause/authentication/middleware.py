from kaffepause.authentication.backend import JSONWebTokenBackend
from kaffepause.authentication.jwt import get_http_authorization


def get_token_argument(request, **kwargs):
    input_fields = kwargs.get("input")
    if isinstance(input_fields, dict):
        kwargs = input_fields
    print(input_fields)

    return kwargs.get("sessionToken", None)


def _authenticate(request):
    is_anonymous = (
        not hasattr(request, "user") or request.user.is_anonymous
    )  # Django-specific?
    return is_anonymous and get_http_authorization(request) is not None


# from graphql_jwt.middleware import JSONWebTokenMiddleware
class JSONWebTokenMiddleware:
    def __init__(self):
        self.backend = JSONWebTokenBackend()

    def resolve(self, next, root, info, **kwargs):
        context = info.context
        if _authenticate(context):
            user = self.backend.authenticate(request=context, **kwargs)
            if user is not None:
                context.user = user

        return next(root, info, **kwargs)
