from kaffepause.authentication.backend import JSONWebTokenBackend
from kaffepause.authentication.jwt import get_http_authorization


def _authenticate(context):
    is_anonymous = not hasattr(context, "user") or context["user"].is_anonymous
    return (
        is_anonymous and get_http_authorization(request=context["request"]) is not None
    )


# from graphql_jwt.middleware import JSONWebTokenMiddleware
class JSONWebTokenMiddleware:
    def __init__(self):
        self.backend = JSONWebTokenBackend()

    def resolve(self, next, root, info, **kwargs):
        context = info.context
        request = context["request"]

        if _authenticate(context):
            user = self.backend.authenticate(request=request, **kwargs)
            if user is not None:
                context["user"] = user

        return next(root, info, **kwargs)
