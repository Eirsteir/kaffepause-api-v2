from starlette_graphene3 import GraphQLApp, make_graphiql_handler

from kaffepause.api.schema import schema
from kaffepause.authentication.middleware import JSONWebTokenMiddleware
from kaffepause.authentication.models import UnauthenticatedUser
from kaffepause.core.config import settings


async def context(request):
    return dict(request=request, user=UnauthenticatedUser())


if settings.DEBUG:
    graphql_app = GraphQLApp(
        schema,
        middleware=[JSONWebTokenMiddleware()],
        context_value=context,
        on_get=make_graphiql_handler(),
    )
else:
    graphql_app = GraphQLApp(
        schema, context_value=context, middleware=[JSONWebTokenMiddleware()]
    )
