import logging

from kaffepause.authentication.backend import JSONWebTokenBackend
from kaffepause.authentication.jwt import get_http_authorization

logger = logging.getLogger(__name__)


def _authenticate(context):
    is_anonymous = "user" not in context or context["user"].is_anonymous
    return (
        is_anonymous and get_http_authorization(request=context["request"]) is not None
    )


class JSONWebTokenMiddleware:
    def __init__(self):
        self.backend = JSONWebTokenBackend()

    def resolve(self, next, root, info, **kwargs):
        context = info.context
        request = context["request"]

        if _authenticate(context):
            user = self.backend.authenticate(request=request, **kwargs)

            if user is not None:
                logger.debug(f"Successfully authenticated user: {user.email}")
                context["user"] = user

        return next(root, info, **kwargs)
