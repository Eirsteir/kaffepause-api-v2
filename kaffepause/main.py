from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette_graphene3 import GraphQLApp, make_graphiql_handler

from kaffepause.api.schema import schema
from kaffepause.core.config import settings
from kaffepause.database import lifespan


def get_application():
    _app = FastAPI(
        title=settings.PROJECT_NAME,
        lifespan=lifespan,
        open_api_url=None,
        debug=settings.DEBUG,
    )

    if settings.DEBUG:
        _app.mount("/graphql", GraphQLApp(schema, on_get=make_graphiql_handler()))
    else:
        app.mount("/graphql/", GraphQLApp(schema))

    _app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return _app


if settings.DEBUG:
    import sentry_sdk

    sentry_sdk.init(
        dsn=settings.SENTRY_DSN,
        traces_sample_rate=1.0,
    )

app = get_application()
